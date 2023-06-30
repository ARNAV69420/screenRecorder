export RECORDER_WORK_DIR="/home/arnav/screenRecorder"
while getopts ":ha:s:t:" option; do
  case $option in
    h)
      echo "flags: "
      echo "-a : for recording with audio, pass fps as argument"
      echo "-s : for silent recording , pass fps as argument"
      echo "-t : for timelapse videos, pass intervals to capture frames"
      exit 0
      ;;
    a)
      g++ $RECORDER_WORK_DIR/waudio.c++ -o waudio
      waudio $OPTARG screencast_with_audio.mp4 &>/dev/null  
      ;;
    s)
      python3 $RECORDER_WORK_DIR/woaudio.py $OPTARG &>/dev/null
      ;;
    t)
      python3 $RECORDER_WORK_DIR/timelapse.py $OPTARG &>/dev/null
      ;;
    *)
      echo "usage [-h] [-a fps] [-s fps] [-t interval]"
      exit 1
      ;;
  esac
done

