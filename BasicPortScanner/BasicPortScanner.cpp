#include <iostream>
#include <winsock2.h> // For Windows sockets
#include <ws2tcpip.h> // For Windows sockets (more modern)
#include <thread>   // For threading (C++11 and later)
#include <future>   // For async operations (C++11 and later)
#include <vector>   // For storing threads
using namespace std;
#pragma comment(lib, "ws2_32.lib") // Link the Winsock library

bool scan_port(const string& ip, int port) {
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        cerr << "WSAStartup failed" << endl;
        return false;
    }

    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) {
        cerr << "Socket creation failed" << endl;
        WSACleanup();
        return false;
    }

    sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    inet_pton(AF_INET, ip.c_str(), &addr.sin_addr); //use inet_pton for IPv4/IPv6

    //set a timeout(important!)
    int timeout = 1000; //1 second
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&timeout, sizeof(timeout));
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, (const char*)&timeout, sizeof(timeout));

    if (connect(sock, (sockaddr*)&addr, sizeof(addr)) == 0) {
        closesocket(sock);
        WSACleanup();
        return true; //port is open
    }
    else {
        closesocket(sock);
        WSACleanup();
        return false; // port is closed(or error)
    }
}

int main()
{
    string ip;
    int start_port, end_port;

    cout << "Enter target IP address: ";
    cin >> ip;
    cout << "Enter starting port: ";
    cin >> start_port;
    cout << "Enter ending port: ";
    cin >> end_port;


    vector<future<bool>> futures; //store future results

    for (int port = start_port; port <= end_port; ++port) {
        //use async for threading (better than raw threads in this case)
        futures.push_back(async(launch::async, scan_port, ip, port));
    }

    for (int i = 0;i < futures.size();++i) {
        int current_port = start_port + i; //store current port number
        bool is_open = futures[i].get();
        if (is_open) { // Get the result (this will block until it's available)
            cout << "Port " << start_port + i << " is open" << endl;
        }
        else {
            cout << "Port " << current_port << " is closed" << endl;
        }
    }

    cout << "Scan complete." << endl;
    return 0;
}

