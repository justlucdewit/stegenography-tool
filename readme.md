# Stegenography-tool

a tool for hiding data inside of images

## Quick test:
- do `python steg-encode.py test/message.txt test/covid19.png` to generate the test/covid19-output.png file, which has the file encoded
- now delete the original test/message.txt and test/covid19.png image
- now do `python steg-decode.py test/covid19-output.png` to retrieve the message.txt file again

## Encoding
```
python steg-encode.py <file you want to hide> <image into which you want to hide the file>
```

## Decoding
```
python steg-decode.py <image with file encoded into it>
```