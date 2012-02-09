# This script will be sourced with the following variables set
#
# TOF_HOME    location of the git repository
# TOF_CONFIG  configuration file
# GIT_REMOTE  name of remote where to pull new objects
# SSD         start-stop-daemon with pid argument
# CHANGES     where to write changelog
# action      in update,start,stop

usage() {
        echo RTFM
        exit 1
}

if [ $# -lt 1 ]
then
        usage
fi

case "$action" in
        update )
                cd "$TOF_HOME"
                unset GIT_DIR
                git fetch "$GIT_REMOTE"
                git log --oneline -5 "remotes/$GIT_REMOTE/master..master" > "$CHANGES"
                git merge --ff-only "$GIT_REMOTE/master"
                ;;
        start )
		find "$TOF_HOME" -name '*.pyc' -delete
                $SSD \
                        --chdir $TOF_HOME \
                        --background \
                        --make-pidfile \
                        --exec $TOF_HOME/bot.py \
                        -S -- -x "$TOF_CONFIG"
                ;;
        stop )
                $SSD -K
                ;;
        * )
                usage
                ;;
esac
