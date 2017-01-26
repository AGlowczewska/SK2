#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <signal.h>
#include <pthread.h>
#include <iostream>
#include <sstream>
#include <vector>
#include <math.h>

#define BUF_SIZE 1024
#define SERVER_PORT 2057
#define QUEUE_SIZE 5

using namespace std;
pthread_mutex_t myMutex = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mySendMutex = PTHREAD_MUTEX_INITIALIZER;
int Clients = 0; // number of connected clients

 struct Thread{
    int Id;
    string Name;
};

Thread THREADS[QUEUE_SIZE]; // list of threads

/*Function for sending list of currently connected clients to server */
void update(){
    char myBuffer[BUF_SIZE];
    bzero(myBuffer, BUF_SIZE);
    stringstream ss;
    ss << 1 << Clients << ' ';
    for (int i=0; i < QUEUE_SIZE; i++){
        if (THREADS[i].Id != 0)
            ss << THREADS[i].Id << " " << THREADS[i].Name << " ";
    }
    string message = ss.str();
    cout << "(Update func): Updating to all:" << message << endl;
    for (int i=0; (unsigned)i< message.size(); i++) myBuffer[i] = message[i];
    for (int i=0; i < QUEUE_SIZE; i++)
        if (THREADS[i].Id != 0)
            write(THREADS[i].Id, myBuffer, BUF_SIZE);
}

// function finds a i (in THREADS[i]) where the descriptor is
int find(int descriptor){
    for (int i=0; i < QUEUE_SIZE; i++){
        if (THREADS[i].Id == descriptor) return i;
    }
    cerr << "(Find func): NOT FOUND IN GLOBAL TABLE" << endl;
    exit(1);
}

void killclient(int myNumber){
    pthread_mutex_lock(&myMutex);
    THREADS[myNumber].Id = 0;
    cout << "(Kill func): Client disconnected:" << THREADS[myNumber].Name << endl;
    THREADS[myNumber].Name = ' ';
    Clients--;
    cout << "(Kill func): Number of current connections:" << Clients << endl;
    if (Clients > 0 )
        update();
    else {
        cout << "(Kill func): No clients connected. Waiting for clients to join." << endl;
    }
    pthread_mutex_unlock(&myMutex);
}

/*Function for reading from the socket */
void *reading(void *client){
    char myBuffer[BUF_SIZE];
    char myBuffer2[BUF_SIZE];
    int nBytes; int nBytes2;

    struct Thread *myThread = (struct Thread*)client;
    int myNumber = find((*myThread).Id);
    cout << "(Read func): New thread for the client nr: " << myNumber << ", Name: " << THREADS[myNumber].Name << endl;

    while(1) {

        bzero(myBuffer, BUF_SIZE);
        nBytes = read(THREADS[myNumber].Id, myBuffer, BUF_SIZE);
        if (nBytes == 0) {
            cerr << "(Read func): Receiving header error" << endl;
            killclient(myNumber);
            pthread_exit(NULL);
        }

        stringstream ss;
        for (int i=0; i < BUF_SIZE; i++) ss << myBuffer[i];
        string message = ss.str();
        int lodbiorcow = message.find(' ') - 1;
        ss.str(string());

        int sendto[6]; for (int i=0; i<6; i++) sendto[i] = 0; //last position is length of file

        int i = 3;
        for( int j =0; j < lodbiorcow+1; j++){
            while (myBuffer[i] != ' '){
                sendto[j] = (sendto[j]*10) + (int)(myBuffer[i]) - 48;
                i++;
            }
            i++;
        }

        cout << "(Read func): Message header: " << myBuffer << endl;
        cout << "(Read func): Received message from: " << myNumber << " and will be sent to " << lodbiorcow <<" clients" << endl;
        cout << "(Read func): The length of message is:" << sendto[lodbiorcow] << endl;
        int parts = ceil(sendto[lodbiorcow]/BUF_SIZE) + 1;
        cout << "(Read func): The message is splitted in " << parts << " parts." << endl;
        for(int i=0; i < (ceil(sendto[lodbiorcow]/BUF_SIZE))+1; i++) {
            bzero(myBuffer2, BUF_SIZE);
            nBytes2 = read(THREADS[myNumber].Id, myBuffer2, BUF_SIZE);
            if (nBytes2 == 0) {
                cerr << "(Read func): Reading error" << endl;
                killclient(myNumber);
                pthread_exit(NULL);
            }
            for (int j=0; j < BUF_SIZE; j++) ss << myBuffer2[j];
        }

        message = ss.str();
        cout << "(Read func): Message received: " << message << endl;
        ss.str(string());
        ss << '2' << myBuffer[0] << ' ' << THREADS[myNumber].Id ;

        for( int j =0; j < lodbiorcow; j++) ss << ' ' << sendto[j];
        string header = ss.str();
        bzero(myBuffer2, BUF_SIZE);
        for (int i=0; (unsigned)i< header.size(); i++) myBuffer2[i] = header[i];
        cout << "(Read func): Sending header: " << myBuffer2 << endl;

        pthread_mutex_lock(&mySendMutex);
        for( int j =0; j < lodbiorcow; j++)
            write(sendto[j], myBuffer2, BUF_SIZE);
        ss.str(string());


        for (int i =0; i < parts; i ++) {
            bzero(myBuffer, BUF_SIZE);
            for(int j = 0; j < BUF_SIZE; j++)
                if (message.length() < (unsigned)(j+(i*1024)))
                    myBuffer[j] = message[j+(i*1024)];
                else break;
            for( int j =0; j < lodbiorcow; j++) {
                cout << myBuffer << endl;
                write(sendto[j], myBuffer, BUF_SIZE);
            }
        }
        pthread_mutex_unlock(&mySendMutex);
        cout << "(Read func): Message sent to clients" << endl;
    }

}

/* Function for connecting clients to server */
void connect(int mySocket){
    int myConnection;
    char myBuffer[BUF_SIZE];
    //cout <<"before accept" <<endl;
    myConnection = accept(mySocket,NULL, NULL);
    //cout << "accepted" << endl;
    struct Thread data;
    data.Id = myConnection;
    if (myConnection < 0) {
        cerr << "ERROR: Can't create connection socket." << endl;
        exit(1);
    } else {
        cout << "(Connect func): Connection socket created:" << myConnection << endl;
        bzero(myBuffer, BUF_SIZE);
        read(myConnection, myBuffer, BUF_SIZE);
        for (int i =0; i <BUF_SIZE; i ++)
            if( myBuffer[i+2] !=0 ) {
                myBuffer[i] = myBuffer[i+2];
            } else {
                myBuffer[i] = 0;
            }

        data.Name = myBuffer;
        cout << "(Connect func): Client login:" << data.Name << endl;
    }

    pthread_t client;
    if (pthread_create(&client, NULL, reading, (void *)&data) == 1){
        cerr << "ERROR: Creating thread" << endl;
        exit(1);
    } else {
        pthread_mutex_lock(&myMutex);
        for (int i=0; i < QUEUE_SIZE; i++)
            if (THREADS[i].Id == 0) {
                THREADS[i].Id = data.Id;
                THREADS[i].Name = data.Name;
                cout << "(Connect func): Nr klienta: " << i << endl;
                break;
            }
        Clients++;
        cout << "(Connect func): Number of current connections:" << Clients << endl;
        update();
        pthread_mutex_unlock(&myMutex);
    }

}

int main(int argc, char *argv[]){

    /** Initializing the THREADS table **/
    for (int i=0; i < QUEUE_SIZE; i++){
        THREADS[i].Id = 0;
        THREADS[i].Name = ' ';
    };
    /************************************/


    struct sockaddr_in myServer;
    memset(&myServer, 0, sizeof(struct sockaddr));
    myServer.sin_family = AF_INET;
    myServer.sin_addr.s_addr = htonl(INADDR_ANY);
    myServer.sin_port = htons(SERVER_PORT);

    int mySocket = socket(AF_INET, SOCK_STREAM, 0);
    if(mySocket < 0){
        cerr << "ERROR: Socket creating" << endl;
        exit(1);
    }

    char temp = 1;
    setsockopt(mySocket, SOL_SOCKET, SO_REUSEADDR, (char*)&temp, sizeof(temp));
    cout << "(Main func): Socket created" << endl;

    int myBind = bind(mySocket, (struct sockaddr*)&myServer, sizeof(struct sockaddr));
    if(myBind < 0 ){
        cerr << "ERROR: Binding IP and port to socket" << endl;
        exit(1);
    }
   cout << "(Main func): Socket binded..." << endl;

    int myListen = listen(mySocket, QUEUE_SIZE);
    if (myListen < 0 ){
        cerr << "ERROR: Queque size"<< endl;
        exit(1);
    }
    cout << "(Main func): Waiting for clients to join..." <<endl;

    while(1){
        if (Clients < 5)
            connect(mySocket);
        else {
            char myBuffer[BUF_SIZE];
            bzero(myBuffer, BUF_SIZE);
            int temp = accept(mySocket,NULL, NULL);
            cout << "(Main func): disconnecting next client";
            read(temp, myBuffer, BUF_SIZE);
            cout << myBuffer << endl;
            bzero(myBuffer, BUF_SIZE);
            write(temp, myBuffer, BUF_SIZE);
        }
    }

    return 0;
}