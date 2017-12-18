import argparse
import subprocess

def start_tunnel(localport, service_address, service_port, keyfile, username, ssh_address,  logfile):
    # kill existing tunnel process
    subprocess.call("kill $(ps -ef | grep 'ssh -N -L' | awk {'print$2'}) &", shell=True)
    # Start new one
    subprocess.call('ssh -N -L {0}:{1}:{2} -i {3} {4}@{5} -vvv >{6} 2>&1 &'.format(localport, service_address, service_port, keyfile, username, ssh_address, logfile), shell=True)

if __name__ == "__main__":
    ### parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-lp", "--local-port", dest="localport", default="", required=True, help="")
    parser.add_argument("-sa", "--service-address", dest="service_address", default="", help="")
    parser.add_argument("-sp", "--service-port", dest="service_port", default="", help="")
    parser.add_argument("-kf", "--keyfile", dest="keyfile", default="", help="")
    parser.add_argument("-u", "--username", dest="user", default="", help="")
    parser.add_argument("-ssh", "--ssh-address", dest="ssh_address", default="", help="")
    parser.add_argument("-l", "--logfile", dest="logfile", default="09-03-2017", help="")
    args = parser.parse_args()
    ### read xml query payload
    start_tunnel(args.localport, args.service_address, args.service_port, args.keyfile, args.user, args.ssh_address, args.logfile)
    ### Print to standard output
