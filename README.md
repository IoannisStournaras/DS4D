# Data Science for Design

Repo for Group Assignment and Individual Projects

## Data Characteristics

The dataset consists of 46 columns and 1058 rows. Each line reports information about the performance of players of a certain team during a certain game. In particular:

- the "team" variable shows the name of the team in question. Since the teams have played more than one game, a specific team is present several times in the "team" column (example: row 1 refers to a game of Denmark, as well as row 73 which refers to another match played by Denmark )

- the "cluster" variable indicates the group (or cluster) to which the team has been assigned on that specific occasion. I remind you that when for example we said that Spain was part of the group of front-runners, it was intended that in most cases Spain had been assigned to that group, but it is not that every single match of Spain has been included in the group of the front-runners. So it may very well be that in some matches Spain is placed in Cluster 1, others in Cluster 2 etc.

- the other 44 variables indicate the closeness (C1, C2, ... C11) the betweenness (B1, B2, .. B11), the median position along the X axis, that is the "long side" of the field (X1, X2 , .. X11) and the median position along the Y axis, ie the "short" side of the field (Y1, Y2, .. Y11) of the 11 players.

So, in summary, each row shows the 4 indicators (betweeness, closeness, median of X and median of Y) for each of the 11 players of each team - which, on that specific occasion, showed a type of performance typical of cluster number you see written in the "cluster" cell.

Looking at the table, I used the comma to divide the whole part of the number from the decimal part, i.e. the number "3,598" is NOT three thousand five hundred and ninety eight but three point five hundred and ninety eight.

## Link to the API deployed on Heroku

https://dfd-fifa18.herokuapp.com/fifa18?fbclid=IwAR1g5Xmi7rBMfHIqZzb_dNHUK_t3AocJ-1zEw0jeIYYQHeffBBkZfjIqkGw
