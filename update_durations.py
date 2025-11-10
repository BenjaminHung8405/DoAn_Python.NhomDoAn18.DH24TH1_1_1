#!/usr/bin/env python3
"""
Script to update track durations in the database with real durations from audio files.
"""

import os
import sys
from mutagen.mp3 import MP3
from io import BytesIO
import urllib.request

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Database.Database import get_all_tracks, get_connection, release_connection


def get_project_root():
    """
    Get the project root directory.
    """
    return os.path.dirname(os.path.abspath(__file__))


def get_real_duration_from_file(file_path):
    """
    Get the real duration from an audio file using mutagen.
    Returns duration in seconds, or None if failed.
    """
    try:
        # If it's a relative path starting with 'songs/', make it absolute
        if file_path.startswith('songs/'):
            project_root = get_project_root()
            file_path = os.path.join(project_root, file_path)

        # Check if file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None

        # Get duration using mutagen
        audio = MP3(file_path)
        duration = audio.info.length
        return int(duration)  # Convert to integer seconds

    except Exception as e:
        print(f"Error getting duration from file {file_path}: {e}")
        return None


def get_real_duration_from_url(url):
    """
    Get the real duration from a remote URL using mutagen.
    Returns duration in seconds, or None if failed.
    """
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        byte_audio = BytesIO(resp.read())

        # Get duration using mutagen
        audio = MP3(byte_audio)
        duration = audio.info.length
        return int(duration)  # Convert to integer seconds

    except Exception as e:
        print(f"Error getting duration from URL {url}: {e}")
        return None


def update_track_duration(track_id, new_duration):
    """
    Update the duration_seconds field for a track in the database.
    """
    if new_duration is None:
        print(f"Skipping track {track_id} - no valid duration")
        return False

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE tracks
            SET duration_seconds = %s
            WHERE track_id = %s
        """, (new_duration, track_id))

        conn.commit()
        cur.close()
        return True

    except Exception as ex:
        if conn:
            conn.rollback()
        print(f'Error updating track {track_id}: {ex}')
        return False
    finally:
        if conn:
            release_connection(conn)


def main():
    """
    Main function to update all track durations.
    """
    print("🔄 Starting duration update process...")

    # Get all tracks from database
    tracks = get_all_tracks()
    if not tracks:
        print("❌ No tracks found in database")
        return

    print(f"📊 Found {len(tracks)} tracks to process")

    updated_count = 0
    failed_count = 0

    for i, track in enumerate(tracks, 1):
        track_id = track.get('track_id')
        title = track.get('title', 'Unknown')
        location = track.get('location', '')
        current_duration = track.get('duration_seconds', 0)

        print(f"\n🎵 Processing {i}/{len(tracks)}: {title}")
        print(f"   Current duration: {current_duration}s")
        print(f"   Location: {location}")

        # Determine if it's a local file or remote URL
        real_duration = None
        if location.startswith('songs/') and location.endswith('.mp3'):
            # Local file
            real_duration = get_real_duration_from_file(location)
        elif location.startswith('http://') or location.startswith('https://'):
            # Remote URL
            real_duration = get_real_duration_from_url(location)
        else:
            print(f"   ⚠️  Unknown location format: {location}")
            failed_count += 1
            continue

        if real_duration is None:
            print("   ❌ Failed to get real duration")
            failed_count += 1
            continue

        print(f"   Real duration: {real_duration}s")

        # Only update if the duration is different
        if real_duration != current_duration:
            if update_track_duration(track_id, real_duration):
                print("   ✅ Updated successfully")
                updated_count += 1
            else:
                print("   ❌ Failed to update")
                failed_count += 1
        else:
            print("   ⏭️  Duration already correct")

    print("\n📈 Update Summary:")
    print(f"   ✅ Updated: {updated_count} tracks")
    print(f"   ❌ Failed: {failed_count} tracks")
    print(f"   ⏭️  Skipped (already correct): {len(tracks) - updated_count - failed_count} tracks")

    if updated_count > 0:
        print("\n🎉 Duration update completed successfully!")
    else:
        print("\nℹ️  No tracks needed updating.")


if __name__ == "__main__":
    main()