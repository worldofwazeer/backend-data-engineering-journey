# Exercise Answers

## Challenge 1
1. `0`, `50`, `100`, `150`
2. 5 pages total (Pages skipping 0, 50, 100, 150, 200 will have data. The last page captures the final 47 records).
3. The request with `skip=250` will return an empty list `[]`.

## Challenge 2
1. It returns an empty list `[]`.
2. A `for` loop assumes you know exactly how many pages exist beforehand. A `while True` loop dynamically adapts to the dataset's true size and terminates exactly when the data runs out, preventing out-of-bounds index errors or missed records.