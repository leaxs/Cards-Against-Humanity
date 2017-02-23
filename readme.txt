Cards Against Humanity, python version by leaxs, v0.2

In order to be useable by the game, carddeck must be in carddeck directory.
The save format is JSON and must be following this scheme:
{
	"calls":
	[
		{"text":["One answer","."]},
    {"text":["Two answer","","."]},       #Each comma create a answer place, it can be place everywhere.
    {"text":["","Three","","."]}          #Each call can have 1, 2 or 3 answer.
  ],
  "responses":
	[
		{"text":["Answer a"]},
    {"text":["Answer b"]},
    {"text":["Answer c"]}
  ]
}
--------- 
Carddeck can be imported from https://www.cardcastgame.com/ with the deck ID.
Default carddeck is extracted from deck from https://www.cardcastgame.com/
Currently need a python interpreter with compiler to be played.
