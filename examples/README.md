# Examples

## Running the examples
```
# first run against local file system
cd <exampledir>/local
pip install ../../..
./main.py LCL_SRC LCL_DEST [-w]

# now run the same operation against S3
cd ../s3
./main.py S3_SRC S3_DEST [-w]
```

## Disemvowel
The function `disemvowel.py` removes all the vowels from one file and stores
the result in another.

The `local` directory contains a program that applies the `disemvowel` function
to files in the local file system.

The `s3` directory contains a program that applies the `disemvowel` function
to files in the S3 file system.

