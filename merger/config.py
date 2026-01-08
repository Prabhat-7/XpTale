class Config:
    # ----------------------------
    # CONFIGURATION
    # ----------------------------
    INPUT_FOLDER = "input"
    NORMALIZED_FOLDER = "temp/normalized"   # ALL videos
    CONVERTED_FOLDER = "temp/converted"     # ONLY converted images

    FILES_TXT = "temp/files.txt"
    OUTPUT_FILE = "output/merged.mp4"

    # Photo video settings
    PHOTO_DURATION = 3  # seconds per photo
    FPS = 30
    RESOLUTION = "1920:1080"
    VIDEO_CODEC = "libx264"
    AUDIO_CODEC = "aac"
    CRF = "23"
    PRESET = "fast"

    # Supported formats
    VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv"]
    PHOTO_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".heic"]
