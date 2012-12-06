user {'tofbot':
    ensure => present,
}

vcsrepo {'/usr/local/src/tofbot':
    ensure   => latest,
    provider => git,
    source   => 'https://github.com/martinkirch/tofbot.git',
    revision => 'master',
}

file {'tofbot-init':
    path      => '/etc/init.d/tofbot',
    source    => '/usr/local/src/tofbot/tofbot.init',
    subscribe => Vcsrepo['/usr/local/src/tofbot'],
    mode      => 0755,
}

file {'/var/log/tofbot':
    ensure => directory,
    owner  => 'tofbot',
}

service {'tofbot':
    ensure    => running,
    require   => User['tofbot'],
    subscribe => [File['tofbot-init'],
                  Vcsrepo['/usr/local/src/tofbot'],
    ],
}

package {'python':
    ensure => installed,
}
