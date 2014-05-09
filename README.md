This is tofbot
==============

configuration files in tofconfigs/

launch for a given configuration like this:

    python bot.py -x tofconfigs/localhost.conf

more help about command line arguments:

    python bot.py -h

Deployment
----------

You need:

  - ansible
  - a remote machine. Let's call it tofbox (it can be an alias in
    ~/.ssh/config). All you need there is a python 2 interpreter, and a
    passwordless sudo for a "admin" user (feel free to edit the .yml).

Let's prepare the local environment.

    cat >> devops/hosts << EOF
    [ircservers]
    tofbox
    EOF

    cat >> devops/templates/default.conf << EOF
    !server irc.freenode.net
    !port 6667
    !nick blabla
    !name blabla
    !chan #blabla
    EOF

Then we can install stuff on the remote machine.

    ansible-playbook -i devops/hosts devops/provision.yml

Then every time you want to deploy:

    ansible-playbook -i devops/hosts devops/deploy.yml

That's all, folks.
