#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <queue>
#include <vector>
#include <cstring>

using namespace std;


/* Spacedeli */
/* Melistas Thomas */
/* Patris Nikolas */


struct squareCord
{
    int squareX;
    int squareY;
};

struct spaceSquare
{
  /* True if pizza in on wrap drive else false */
    bool pizzaMode;
    int timeCost;
    string spacePath;
    squareCord square;

    bool operator<(const spaceSquare & otherSquare) const
    {
        return timeCost > otherSquare.timeCost;
    }
};


/* Dynamic allocation memory for user input */
void makeMap (vector<vector<char> > & spaceMap, int & startX, int & startY, int & endX, int & endY, char * fileName) {
    FILE * filePointer;
    char nextChar;

    if ((filePointer = fopen(fileName,"r")) == NULL) {
        printf("file: doesn't exist");
        exit(1);
    }

    for (int i = 0; !feof(filePointer); i++) {
        vector < char > rowVector;
        for (int j = 0; true; j++) {

            if (fscanf(filePointer,"%c",&nextChar) != 1) break;

            /* Newline exception */
            if (nextChar == '\n') break;

            /* Starting point */
            else if (nextChar == 'S') {
                startX = i;
                startY = j;
                rowVector.push_back(nextChar);
            }

            else if (nextChar == 'E') {
                endX = i;
                endY = j;
                rowVector.push_back(nextChar);
            }

            else if (nextChar == '.' || nextChar == 'W' || nextChar == 'X') rowVector.push_back(nextChar);
        }

        spaceMap.push_back(rowVector);
    }
}

/* Find the next move based on moves coordinates */
char findMove (int moveX, int moveY) {
    if (!moveX) {
        if (moveY == 1) {
            return 'R';
        } else {
            return 'L';
        }
    } else if (moveX == 1) {
        return 'D';
    } else {
        return 'U';
    }

}

/* Check if the neighbour square is valid, based on spaceMap limits */
bool validNeighbour(int givenX, int givenY, int limitX, int limitY)
{
    if ((givenX >= 0) && (givenY >= 0) && (givenX < limitX) && (givenY < limitY)) {
        return true;
    } else {
        return false;
    }
}


/* Main function for space bfs */
string spacebfs(vector<vector<char> > & spaceMap, int startX, int startY, int endX, int endY,int limitX, int limitY)
{
    /* Valid movements on spaceMap */
    /* LEFT RIGHT UP DOWN */
    static int xMoves[] = {0, 0, 1, -1};
    static int yMoves[] = {-1, 1, 0, 0};

    priority_queue<spaceSquare> spaceQueue;

    /* A visited with pizza */
    /* B visited without pizza */
    /* X visited both ways */
    char visitedSquares[limitX][limitY];
    memset(visitedSquares, '.', sizeof visitedSquares);

    visitedSquares[startX][startY] = 'A';

    spaceSquare startSquare = {true,0,"",{startX,startY}};
    spaceQueue.push(startSquare);

    while (!spaceQueue.empty())
    {
        /* Get the top item of the queue */
        spaceSquare curSquare = spaceQueue.top();

        squareCord spaceCord = curSquare.square;

        if ((spaceCord.squareX == endX) && (spaceCord.squareY == endY)) {
            if (curSquare.pizzaMode) {
                /* Just found the shortest path */
                cout << curSquare.timeCost << ' ';
                return curSquare.spacePath;
            }
        }

        spaceQueue.pop();

        for (int i = 0; i < 4; i++)
        {
            int newX = spaceCord.squareX + xMoves[i];
            int newY = spaceCord.squareY + yMoves[i];

            /* Check if the new neighbour is valid */
            if (validNeighbour(newX,newY,limitX,limitY))
            {
                if ((spaceMap[newX][newY] != 'X') && (visitedSquares[newX][newY] != 'X'))
                {
                    int prevCost = curSquare.timeCost;

                    string prevPath = curSquare.spacePath;

                    char newMode = findMove(xMoves[i],yMoves[i]);

                    prevPath += newMode;

                    /* Determine the type of square */
                    if (spaceMap[newX][newY] == 'W')
                    {
                        /* Check pizzaMode */
                        if (curSquare.pizzaMode) {
                            /* First time in wormhole */
                            /* I have 2 option to leave the food or continue */
                            spaceSquare inwormHole = {false,prevCost+3,prevPath + 'W',{newX,newY}};

                            spaceSquare overwormHole = {true,prevCost+2,prevPath,{newX,newY}};


                            spaceQueue.push(overwormHole);
                            spaceQueue.push(inwormHole);
                        } else {
                            /* Already in wormhole */
                            /* I have 2 option to get the food or continue until i found the next one */
                            spaceSquare contwormHole = {false,prevCost+1,prevPath,{newX,newY}};

                            spaceSquare outwormHole = {true,prevCost+2,prevPath + 'W',{newX,newY}};

                            spaceQueue.push(outwormHole);
                            spaceQueue.push(contwormHole);
                        }
                    } else {
                        /* Check all the different types of square */
                        if (curSquare.pizzaMode) {
                            spaceSquare newNeighbour = {true,prevCost+2,prevPath,{newX,newY}};

                            if (visitedSquares[newX][newY] == '.') {
                                visitedSquares[newX][newY] = 'A';
                                spaceQueue.push(newNeighbour);
                            } else if (visitedSquares[newX][newY] == 'B') {
                                visitedSquares[newX][newY] = 'X';
                                spaceQueue.push(newNeighbour);
                            }

                        } else {
                            spaceSquare newNeighbour = {false,prevCost+1,prevPath,{newX,newY}};

                            if (visitedSquares[newX][newY] == '.') {
                                visitedSquares[newX][newY] = 'B';
                                spaceQueue.push(newNeighbour);
                            } else if (visitedSquares[newX][newY] == 'A') {
                                visitedSquares[newX][newY] = 'X';
                                spaceQueue.push(newNeighbour);
                            }
                        }

                    }

                }
            }

        }
    }

    return "";
}

int main(int argc, char *argv[])
{
    vector < vector < char > > spaceMap;
    int startX, startY, endX, endY;

    makeMap(spaceMap, startX, startY, endX, endY, argv[1]);

    int limitX,limitY;

    limitX =  spaceMap.size();
    limitY =  spaceMap[0].size();

    string solutionPath = spacebfs(spaceMap, startX, startY, endX, endY, limitX-1, limitY);

    if (solutionPath.size()) {
        cout << solutionPath << '\n';
    } else {
        cout <<"No way \n";
    }

    return 0;

}
