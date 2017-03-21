// text simulation of gameplay

#include <iostream>
#include <string>
#include <cmath>

using namespace std;

void hitball(int, int&, int&);
int findx(char[][500]);
int findy(char[][500]);

int main(){
    char course[500][500];
    int bx = 499;		// ball x location
    int by = 249;		// ball y location
    int hx = 50;
    int hy = 300;
    course[bx][by] = 'o';	//location of tee / starting point of ball
    course[hx][hy] = 'h';	//location of hole
    bool gameplay = true;

    while (gameplay){
    	int mass = 0.0493;		// mass of golf ball, kg
    	hitball(mass, bx, by);
	if (bx == hx && by == hy) gameplay = false;
    }

    cout << "*golf claps*" << endl;
}

void hitball(int mass, int &bx, int &by){
    int dir, theta, power;
    char club;
    cout << "Club [(p)utter, (w)edge, (i)ron, (d)river]: ";
    cin >> club;
    cout << "Angle (45*-135*): ";
    cin >> dir;
    cout << "Power (1-10): ";		//each degree of power is an extra km/h
    cin >> power;

    switch(club){
        case 'p':
	    theta = 0;
	    break;
	case 'w':
	    theta = 15;
	    break;
	case 'i':
	    theta = 45;
	    break;
	case 'd':
	    theta = 60;
	    break;
    }

    bx = 50;
    by = 300;
}

int findx(char course[][500]){
    for (int r = 0; r < 500; r++){
        for (int c = 0; c < 500; c++){
	    if (course[r][c] == 'o') return r;
	}
    }
}

int findy(char course[][500]){
    for (int r = 0; r < 500; r++){
        for (int c = 0; c < 500; c++){
	    if (course[r][c] == 'o') return c;
	}
    }
}
