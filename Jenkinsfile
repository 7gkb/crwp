#!/bin/env groovy
env.GitSourse = 'https://github.com/7gkb/crwp.git'
env.TARGET_BRANCH = '*/master'
env.URi = 'http://192.168.5.186/pcs/'
env.API = 'list.txt'
import groovy.json.*
//String[] SubNet = "${ip_address}".tokenize('.')
//Integer IntSubNet = SubNet[2].toInteger()
//if (IntSubNet == 1) {
//    env.NET = 'OFFICE'
//} else {
//    if (IntSubNet == 5) {
//        env.NET = 'KMIS5'
//    }
//    if (IntSubNet == 108) {
//    env.NET = 'KMIS108'
//    }
//}
pipeline {
   agent any

   stages {
        stage('Get ansible code') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: "${TARGET_BRANCH}"]],
                    skipDefaultCheckout: true,
                    extensions: [[$class: 'CloneOption', timeuot: 240]],
                        extensions: [[$class: 'LocalBranch', localBranch: "master"]],
                    gitTool: 'Default',
                userRemoteConfigs: [[credentialsId: 'github-7gkb', url: "${GitSourse}"]]
                ])
            }
        }
        stage('Update hosts') {
            steps {
                script {
                    String url = "${env.URi}${env.API}"
                    String response = sh(script: "curl -s $url", returnStdout: true).trim()
                    writeFile file: 'responsefile.txt',  text: "${response}"
                    def PlaceJson = readJSON file: 'responsefile.txt', returnPojo: true
                    def HostsLine = []
                    def FileHostsText = ""
                    HostsLine << "[all:vars]\nansible_python_interpreter=/usr/bin/python3\n"
                    HostsLine << "[openvpn]\nsrv1 ansible_host=192.168.1.45\n"
                    HostsLine << "[pcs]"
                    PlaceJson.each { value ->
                        String[] Mac = "${value['mac']}"
                        String[] Host = "${value['host']}"
                        String[] Ip = "${value['ip']}".tokenize('/')
                        if ("${Ip}" != '[]') {
                            if ("${Mac}" != '[]') {
                                String line = "${value['host']}"+' ansible_host='+"${Ip[0]}"
                                HostsLine << line
                            }
                            //else { //закоментировал, т.к. данные тачки не имеют доступ к сети
                                // String line = "${value['host']}"+' ansible_host='+"${Ip}"
                                // HostsLine << line
                            //}
                        FileHostsText = HostsLine.join("\n")
                        }
                    }
                    writeFile file: 'inventory/hosts',  text: "${FileHostsText}"
                }
            }
        }
        stage('Copy files') {
            steps {
                script {
                    sh ("cp -f logo.png roles/crwp/files/crwp/logo.png")
                    sh ("cp -f chwp.sh roles/crwp/files/.chwp/chwp.sh")
                }
            }
        }
        stage('Install the crwp') {
            steps {
                script {
                    try {
                        ansiblePlaybook(
                                        vaultCredentialsId: 'ansible-vault',
                                        inventory: 'inventory/hosts',
                                        playbook: 'playbooks/crwp.yml'
                        )
                    } catch (err) {
                    }
                }
            }
        }
    }
}
