#! /usr/bin/env python2

import ConfigParser
import textwrap
import argparse
import sys
import getpass

class autoInstaller:
    '''
    Deploys and configures OpenShift for the OpenShift in Action test environment
    '''

    def __init__(self, options):

        self.name = 'autoinstaller'
        self.github_url = 'https://github.com/OpenShiftInAction'
        self.autoinstaller_url = "%s/%s" % (self.github_url, self.name)
        self.forum_url = 'https://forums.manning.com/forums/openshift-in-action'
        self._intro_text()
        self.chapter = options.chapter
        self.dry_run = options.dry_run
        self.ansible_playbookdir = './ansible'
        self.inventory = self.ansible_playbookdir + '/hosts'
        self.conf, self.conf_data, self.conf_sections = self._read_conf_file(options.conf_file)
        self.global_confs = self._load_conf_section('global')

        # not all deployment methods need to have a config section
        try:
            self.deployment_confs = self._load_conf_section(self.global_confs['deployment'])
        except ConfigParser.NoSectionError:
            print("* No %s options found - none loaded" % self.global_confs['deployment'] )
            self.deployment_confs = dict()
        self._deploy_ocp()

    def _read_conf_file(self, fh):
        '''
        loads the config file (default is autoinstaller.conf)
        and returns a ConfigParser object for the file as well
        as a list of the config sections for logic purposes
        Can be used to get different sections as needed
        '''
        conf = ConfigParser.ConfigParser()
        conf_data = conf.read(fh)
        conf_sections = conf.sections()
        if self.dry_run:
            print("*** Dry Run Mode Enabled - no actual systems will be deployed\n")
        print("* Using %s for configuration" % conf_data[0])

        return conf, conf_data, conf_sections

    def _load_conf_section(self, section):
        '''
        returns the configs for a given section of the config file
        '''
        dict1 = dict()
        options = self.conf.options(section)
        for option in options:
            try:
                dict1[option] = self.conf.get(section, option)
            except:
                print("* Unable to load %s" % option)
                dict1[option] = None
        print("* Loaded %s configuration options" % section)
        return dict1

    def _build_extravars(self):
        '''
        builds out the extravars string to pass into the autoinstaller playbook
        '''
        evars = str()

        # gather up the global vars
        for k,v in self.global_confs.iteritems():
            evars += "-e %s=%s " % (k,v)
        for k,v in self.deployment_confs.iteritems():
            evars += "-e %s=%s " % (k,v)

        return evars

    def _intro_text(self):
        '''
        a little helpful intro text for the application
        '''

        string = """
Thank you for reading OpenShift In Action. The autoinstaller application is
designed to help you save time when building out your environment to work
through the examples in the book.

A complete feature list and additional information is available in README.md in
this repository.

If you have issues, please contact us on GitHub at {github} or on the Manning
book forum at {forum}.

Thanks again!

The OpenShift In Action Team
""".format(
    github = self.github_url,
    forum = self.forum_url
        )

        print string

    def _create_other_inventory(self):
        '''
        for the 'other' type of installation, you'll supply information about 2 servers that already exist. The IPs will be provided in the config file and the autoinstaller ansible inventory will be created dynamically using this function
        '''

        self.inventory = "/tmp/autoinstaller-other-hosts"
        fh = open('w', self.inventory)

        inv_str = """

        """

        fh.write(inv_str)
        fh.close()

    def _deploy_ocp(self):
        '''
        puts together the command to deploy and executes it if so desired
        '''

        ansible_exec = 'ansible-playbook '
        ansible_exec += ''


def main():
    parser = argparse.ArgumentParser(description='Autoinstaller for OpenShift in Action')
    parser.add_argument('-c', '--chapter', dest="chapter", type=int, default=0, help="chapter you would like to provision through")
    parser.add_argument('--config', dest="conf_file", default="autoinstaller.conf", help="autoinstaller config file, default is autoinstaller.conf")
    parser.add_argument('-d', '--dry-run', dest="dry_run", action="store_true", help="use this option to output the installation command but not launch the installer")

    args = parser.parse_args()
    a = autoInstaller(args)

if __name__ == '__main__':
    main()
