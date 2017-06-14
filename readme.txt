Cards Against Humanity, python version by leaxs, v0.2

In order to be useable by the game, decks must be in carddeck directory.
The save format is JSON and must follow this scheme:
--------- 
{
  "calls":
  [
	{"text":["One answer","."]},
   	{"text":["Two answer","","."]},       #Each comma in text create a answer place, it can be place everywhere.
   	{"text":["","Three","","."]}          #Each call can have 1, 2 or 3 answers.
  ],
  "responses":
  [
	{"text":["Answer a"]},
   	{"text":["Answer b"]},
    	{"text":["Answer c"]}
  ]
}
--------- 
Carddeck can be imported from https://www.cardcastgame.com/ with its ID.
Currently need a python interpreter with a compiler to be played.
