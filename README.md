# midi-artnet
My implementation to connect Ableton Live to ArtNet  lights

## Concept
Read midi using [mido](https://mido.readthedocs.io/) using notes as DMX channels, then send it using StupidArtnet


## hints
```
conda env create --file environment.yml
[or]
conda env update --file environment.yml --prune
```


## dockerized
```bash
docker-compose up --build
```
