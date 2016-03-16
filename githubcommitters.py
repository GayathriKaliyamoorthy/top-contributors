import click;
import logging;
import os;
import pycurl;
from StringIO import StringIO;
from io import BytesIO
import json;
import re; 
import sys;

URL = "https://api.github.com";
conn = pycurl.Curl();
conn.setopt(conn.FOLLOWLOCATION, True);
logging.basicConfig(level=logging.INFO, filename="committers.log");
logger = logging.getLogger('githubcommiters');

def invokeURL(url):
    if not url:
        logger.warning("An URL must be passed to invokeURL");
        return;
    buffer = BytesIO();
    conn.setopt(conn.URL, url);
    conn.setopt(conn.WRITEFUNCTION, buffer.write);
    conn.perform();
    content = buffer.getvalue().decode('utf-8');
    return json.loads(content);

def generateSearchURL(organization):
    if not organization:
        logger.warning("A value must be passed to generate organization URL");
        return None;
    else:
        return URL + "/search/repositories?q=user:" + str(organization) + "&sort=forks&order=desc";

def getPopularRepos(organization):
    if not organization:
        logger.warning("Organization value not present");
        return;
    url = generateSearchURL(organization);
    if url is None:
        logger.warning("URL for the " + organization +" is Null");
        return;
    popularRepos = invokeURL(url);
    return popularRepos;

def getTopCommittees(popularRepos, length, maxcommitters):
    output = {};
    for i in xrange(0,length):
        repoName = popularRepos['items'][i]['full_name'].split('/')[1];
        output[repoName] = {};
        committers = invokeURL(str(popularRepos['items'][i]['contributors_url']));
        noOfCommitters = maxcommitters;
        if len(committers) < maxcommitters:
            noOfCommitters = len(committers);
            logger.info("Number of committers: " + str(noOfCommitters) +" in the repo"  + str(repoName) + \
                    " is less then maxcommitters: " + str(maxcommitters));
        for j in xrange(0, noOfCommitters):
            output[repoName][committers[j]['login']] = committers[j]['contributions'];
    return output;



@click.command()
@click.argument('org', required=True)
@click.argument('repos',  required=True)
@click.argument('committees',  required=True)
def printTopCommitter(org, repos, committees):
    ''' Takes an organization as parameter. 
        And prints the committees who have maximum commits in org's
        popular repositories. [popularity == max number of forks]
    '''
    repocount = int(repos);
    maxcommitters = int(committees);
    popularRepos = getPopularRepos(org);	
    noOfRepos = len(popularRepos['items']);
    length = repocount;
    if noOfRepos < repocount:
        logger.info("Number of repos in this " + str(org) + " is less than " + str(repocount));
        length = noOfRepos;
    topCommittees = getTopCommittees(popularRepos, length, maxcommitters);
    print(json.dumps(topCommittees, indent=4, separators=(',',':')));


'''
if __name__ == '__main__':
	printTopCommiter();
'''

	
