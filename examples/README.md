# Examples

## Running the examples
```
# first run against local file system
cd <exampledir>/local
pip install ../../..
./main.py

# now run the same operation against S3
cd ../s3
./main.py
```

## Disemvowel
Removes all the vowels from one file and stores the result in another.

The `local` directory a local file and stores the result in a local file.

## S3-Disemvowel
Removes all the vowels from a file in one S3 bucket and stores the result in
another S3 bucket.

