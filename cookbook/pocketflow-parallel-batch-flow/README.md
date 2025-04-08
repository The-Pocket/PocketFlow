# Parallel Image Processor

Demonstrates how AsyncParallelBatchFlow processes multiple images with multiple filters >8x faster than sequential processing.

## Features

  ```mermaid
  graph TD
      subgraph AsyncParallelBatchFlow[Image Processing Flow]
          subgraph AsyncFlow[Per Image-Filter Flow]
              A[Load Image] --> B[Apply Filter]
              B --> C[Save Image]
          end
      end
  ```
  
- Processes images with multiple filters in parallel
- Applies three different filters (grayscale, blur, sepia)
- Shows significant speed improvement over sequential processing
- Manages system resources with semaphores

## Run It

```bash
pip install -r requirements.txt
python main.py
```

## Output

```=== Processing Images in Parallel ===
Parallel Image Processor
------------------------------
Found 3 images:
- images/bird.jpg
- images/cat.jpg
- images/dog.jpg

Running sequential batch flow...
Processing 3 images with 3 filters...
Total combinations: 9
Loading image: images/bird.jpg
Applying grayscale filter...
Saved: output/bird_grayscale.jpg
...etc

Timing Results:
Sequential batch processing: 13.76 seconds
Parallel batch processing: 1.71 seconds
Speedup: 8.04x

Processing complete! Check the output/ directory for results.
```

## Key Points

- **Sequential**: Total time = sum of all item times
  - Good for: Rate-limited APIs, maintaining order

- **Parallel**: Total time ≈ longest single item time
  - Good for: I/O-bound tasks, independent operations 
