imageNAME="pocket_square"
imageTAG="0.0.1"
echo "Building $imageNAME:$imageTAG"

# build image
docker build . --progress=plain -t "$imageNAME":"$imageTAG" -t "$imageNAME":latest
