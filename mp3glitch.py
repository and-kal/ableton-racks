import argparse
import random

# Glitching function to apply random byte-level corruption
def glitch_bytes(body, glitch_count=1000):
    for _ in range(glitch_count):
        index = random.randint(0, len(body) - 1)
        body[index] = random.randint(0, 255)  # Random byte replacement
    return body

# Glitch segments by chopping, reversing, or repeating
def glitch_segments(body, segment_count=10, bitrate_kbps=128):
    segment_length = int(bitrate_kbps * 0.125)  # Example: segment length based on bitrate
    segments = [body[i:i + segment_length] for i in range(0, len(body), segment_length)]
    
    for _ in range(segment_count):
        segment_index = random.randint(0, len(segments) - 1)
        segment = segments[segment_index]

        # Randomly decide to reverse, repeat, or shuffle this segment
        effect_type = random.choice(['reverse', 'repeat', 'shuffle'])
        
        if effect_type == 'reverse':
            segments[segment_index] = segment[::-1]
        elif effect_type == 'repeat':
            segments[segment_index] = segment * 2  # Repeat segment
        elif effect_type == 'shuffle':
            random.shuffle(segment)
            segments[segment_index] = segment
        
    return b''.join(segments)

# Apply buffer shuffle / beat repeat effects
def buffer_shuffle(body, chunk_ms=250, operations=50, bitrate_kbps=128):
    chunk_size = int(bitrate_kbps * chunk_ms / 8)  # Approximate bytes per chunk based on bitrate
    chunks = [body[i:i + chunk_size] for i in range(0, len(body), chunk_size)]

    for _ in range(operations):
        chunk_index = random.randint(0, len(chunks) - 1)
        chunk = chunks[chunk_index]

        # Randomly reverse or repeat chunks
        effect_type = random.choice(['reverse', 'repeat'])
        
        if effect_type == 'reverse':
            chunks[chunk_index] = chunk[::-1]
        elif effect_type == 'repeat':
            chunks[chunk_index] = chunk * 2  # Repeat chunk

    return b''.join(chunks)

# Parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Glitch an MP3 file with various effects.")
    
    # Input and output files
    parser.add_argument('input_file', type=str, help="The input MP3 file.")
    parser.add_argument('output_file', type=str, help="The output (glitched) MP3 file.")
    
    # Settings for glitches
    parser.add_argument('--glitch_count', type=int, default=1000, help="Number of small byte glitches to apply.")
    parser.add_argument('--segment_count', type=int, default=10, help="Number of larger segment effects (reverse, repeat, etc.).")
    parser.add_argument('--bitrate_kbps', type=int, default=128, help="Bitrate in kbps (for segment calculations).")
    parser.add_argument('--chunk_ms', type=int, default=250, help="Size of chunks in milliseconds (for buffer shuffling).")
    parser.add_argument('--operations', type=int, default=50, help="Number of operations for buffer shuffling.")
    
    return parser.parse_args()

# Main function to apply the glitching effects
def glitch_mp3(args):
    with open(args.input_file, 'rb') as f:
        data = bytearray(f.read())

    # Split header and audio data
    header_bytes = 4096  # You can adjust this to match your MP3 format
    header = data[:header_bytes]
    body = data[header_bytes:]

    # Apply byte-level glitches
    body = glitch_bytes(body, glitch_count=args.glitch_count)

    # Apply larger segment-level edits
    body = glitch_segments(body, segment_count=args.segment_count, bitrate_kbps=args.bitrate_kbps)

    # Apply buffer shuffle / beat repeat effects
    body = buffer_shuffle(body, chunk_ms=args.chunk_ms, operations=args.operations, bitrate_kbps=args.bitrate_kbps)

    # Save to output
    with open(args.output_file, 'wb') as f:
        f.write(header + body)

    print(f"✅ Glitched MP3 saved as: {args.output_file}")

# Run the script with command-line arguments
if __name__ == "__main__":
    args = parse_args()  # Parse command-line arguments
    glitch_mp3(args)  # Pass the arguments to the glitch function