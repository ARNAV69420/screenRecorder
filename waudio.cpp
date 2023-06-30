
#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>
#include <sys/stat.h>
#include <string>
#include <fstream>

using namespace std;

string filename;
string fps;

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cout << "Usage: " << argv[0] << " <fps> <filename>" << endl;
        return 1;
    }

    fps = argv[1];
    filename = argv[2] + string(".mp4");

    mkdir("screenshots", 0777);

    pid_t pid = fork();

    if (pid < 0) {
        cerr << "Fork failed" << endl;
        return 1;
    } else if (pid > 0) {
        while (1) {
            // Keep the main process running
        }
    } else {
        // Close the standard output file descriptor
        close(STDOUT_FILENO);

        // Start capturing audio and frames using FFmpeg
        string command = "ffmpeg -f x11grab -framerate " + fps + " -i :0.0 -f alsa -i default -c:v libx264 -pix_fmt yuv420p -c:a aac -strict experimental " + filename;
        system(command.c_str());

        // Remove the captured screenshots
        string removeCommand = "rm -r screenshots";
        system(removeCommand.c_str());
    }

    return 0;
}

