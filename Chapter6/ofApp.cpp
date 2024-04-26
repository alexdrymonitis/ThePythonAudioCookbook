#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
	ofBackground(0);

	sender.setup(HOST, OUTPORT);
	receiver.setup(INPORT);

	rectSize = ofGetWindowWidth() / 16;

	step = 0;
	metroState = 1;

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 16; j++) {
			toggles[i][j] = 0;
		}
	}

	ofSetLineWidth(2);
}

//--------------------------------------------------------------
void ofApp::update(){
	while(receiver.hasWaitingMessages()) {
		// get the next message
		ofxOscMessage m;
		receiver.getNextMessage(m);
		
		if(m.getAddress() == "/seq") {
			step = m.getArgAsInt32(0);
		}
	}
}

//--------------------------------------------------------------
void ofApp::draw(){
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 16; j++) {
			float x = j * rectSize;
			float y = i * rectSize;
			if ((j == step) && metroState) {
				ofSetColor(255, 0, 0);
			}
			else {
				ofSetColor(200);
			}
			ofDrawRectangle(x+(OFFSET/2), y+(OFFSET/2),
							rectSize-OFFSET, rectSize-OFFSET);
			if (toggles[i][j]) {
				ofSetColor(0);
				ofDrawLine(x+(OFFSET/2), y+(OFFSET/2),
						   x+(rectSize-(OFFSET/2)),
						   y+(rectSize-(OFFSET/2)));
				ofDrawLine(x+(rectSize-(OFFSET/2)), y+(OFFSET/2),
						   x+(OFFSET/2), y+(rectSize-(OFFSET/2)));
				ofSetColor(200);
			}
		}
	}
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){

}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){
	ofxOscMessage m;
	int xIndex;
	int yIndex;
	switch (button) {
		case 0:
			xIndex = x / rectSize;
			yIndex = y / rectSize;
			toggles[yIndex][xIndex] = !toggles[yIndex][xIndex];
			m.setAddress("/seq");
			m.addIntArg(yIndex);
			m.addIntArg(xIndex);
			m.addIntArg(toggles[yIndex][xIndex]);
			sender.sendMessage(m, false);
			break;
		case 2:
			metroState = !metroState;
			m.setAddress("/metro");
			m.addIntArg(metroState);
			sender.sendMessage(m, false);
			break;
		case 1:
			m.setAddress("/reset");
			m.addIntArg(1);
			sender.sendMessage(m, false);
			break;
		default:
			break;
	}
}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 

}
