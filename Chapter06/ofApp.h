#pragma once

#include "ofMain.h"
#include "ofxOsc.h"

#define OFFSET 2
#define HOST "localhost"
#define OUTPORT 12345
#define INPORT 9030

class ofApp : public ofBaseApp{

	public:
		void setup();
		void update();
		void draw();

		void keyPressed(int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y );
		void mouseDragged(int x, int y, int button);
		void mousePressed(int x, int y, int button);
		void mouseReleased(int x, int y, int button);
		void mouseEntered(int x, int y);
		void mouseExited(int x, int y);
		void windowResized(int w, int h);
		void dragEvent(ofDragInfo dragInfo);
		void gotMessage(ofMessage msg);
		
		ofxOscSender sender;
		ofxOscReceiver receiver;

		float rectSize;

		int toggles[3][16];
		int step;
		int metroState;
};
