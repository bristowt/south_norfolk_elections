{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "deletable": true,
    "editable": true
   },
   "source": [
    "# Isle of Wight Local Elections\n",
    "\n",
    "Simple scribbles around Isle of Wight local election candidate data.\n",
    "\n",
    "Reusing code and ideas from:\n",
    "\n",
    "- [Questioning Election Data to See if It Has a Story to Tell](https://blog.ouseful.info/2013/05/05/questioning-election-data-to-see-if-it-has-a-story-to-tell/)\n",
    "- [More Storyhunting Around Local Elections Data Using Gephi – To What Extent Do Candidates Support Each Other?](https://blog.ouseful.info/2013/05/08/more-storyhunting-around-local-elections-data-using-gephi-to-what-extent-do-candidates-support-each-other/)\n",
    "\n",
    "\n",
    "Note that this is a bit ropey and requires you to work through the steps.\n",
    "\n",
    "You may also need to install some additional packages along the way..."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Configuring the scraper source and related filenames"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "#Define scraper sqlite database filename\n",
    "dbname= \"norfolk.sqlite\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "#Optionally delete the previous instance\n",
    "!rm {dbname}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "#Filename for map of candidates\n",
    "mapname='norfolkmap.html'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# The localarea is a search keyword we look for in the address of a companies\n",
    "# that may be associated with directors with the same exact name as a candidate\n",
    "# USe it to just limit the dispplay of companies to companies with addresses that contain that keyword\n",
    "localarea='Norfolk'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "#Candidates filename\n",
    "candsfilename='norfolkcands.csv'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "#Supporters filename\n",
    "supportersfilename='norfolksupporters.csv'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "#filename for companies\n",
    "companiesfilename='norfolkcos.csv'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "#Path to the Notice of election file (note, this can be the path/name of a local file)\n",
    "url='https://www.south-norfolk.gov.uk/sites/default/files/Notice%20of%20Poll.pdf'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "collapsed": true,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "#Companies House API token\n",
    "#Available from: https://developer.companieshouse.gov.uk/api/docs/index/gettingStarted/apikey_authorisation.html\n",
    "CH_API_TOKEN=''"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Install Necessary Packages"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "#Set the path to the pip installer for your Python kernel\n",
    "\n",
    "#It may be available on your path directly, or you may need to specify a path, as below, or pip3\n",
    "#pip='~/anaconda/bin/pip'\n",
    "#pip='pip3'\n",
    "\n",
    "pip='pip'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: lxml in /usr/local/lib/python3.5/site-packages\n",
      "Requirement already satisfied: scraperwiki in /usr/local/lib/python3.5/site-packages\n",
      "Requirement already satisfied: alembic in /usr/local/lib/python3.5/site-packages (from scraperwiki)\n",
      "Requirement already satisfied: sqlalchemy in /usr/local/lib/python3.5/site-packages (from scraperwiki)\n",
      "Requirement already satisfied: six in /usr/local/lib/python3.5/site-packages (from scraperwiki)\n",
      "Requirement already satisfied: requests in /usr/local/lib/python3.5/site-packages (from scraperwiki)\n",
      "Requirement already satisfied: Mako in /usr/local/lib/python3.5/site-packages (from alembic->scraperwiki)\n",
      "Requirement already satisfied: python-editor>=0.3 in /usr/local/lib/python3.5/site-packages (from alembic->scraperwiki)\n",
      "Requirement already satisfied: MarkupSafe>=0.9.2 in /usr/local/lib/python3.5/site-packages (from Mako->alembic->scraperwiki)\n",
      "Requirement already satisfied: pandas in /usr/local/lib/python3.5/site-packages\n",
      "Requirement already satisfied: pytz>=2011k in /usr/local/lib/python3.5/site-packages (from pandas)\n",
      "Requirement already satisfied: numpy>=1.7.0 in /usr/local/lib/python3.5/site-packages (from pandas)\n",
      "Requirement already satisfied: python-dateutil>=2 in /usr/local/lib/python3.5/site-packages (from pandas)\n",
      "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.5/site-packages (from python-dateutil>=2->pandas)\n",
      "Requirement already satisfied: networkx in /usr/local/lib/python3.5/site-packages\n",
      "Requirement already satisfied: decorator>=3.4.0 in /usr/local/lib/python3.5/site-packages (from networkx)\n",
      "Requirement already satisfied: geocoder in /usr/local/lib/python3.5/site-packages\n",
      "Requirement already satisfied: ratelim in /usr/local/lib/python3.5/site-packages (from geocoder)\n",
      "Requirement already satisfied: six in /usr/local/lib/python3.5/site-packages (from geocoder)\n",
      "Requirement already satisfied: requests in /usr/local/lib/python3.5/site-packages (from geocoder)\n",
      "Requirement already satisfied: click in /usr/local/lib/python3.5/site-packages (from geocoder)\n",
      "Requirement already satisfied: decorator in /usr/local/lib/python3.5/site-packages (from ratelim->geocoder)\n",
      "Requirement already satisfied: folium in /usr/local/lib/python3.5/site-packages\n",
      "Requirement already satisfied: Jinja2 in /usr/local/lib/python3.5/site-packages (from folium)\n",
      "Requirement already satisfied: branca in /usr/local/lib/python3.5/site-packages (from folium)\n",
      "Requirement already satisfied: six in /usr/local/lib/python3.5/site-packages (from folium)\n",
      "Requirement already satisfied: MarkupSafe>=0.23 in /usr/local/lib/python3.5/site-packages (from Jinja2->folium)\n",
      "Requirement already satisfied: uk-postcode-utils in /usr/local/lib/python3.5/site-packages\n"
     ]
    }
   ],
   "source": [
    "#Install required packages\n",
    "!{pip} install lxml\n",
    "!{pip} install scraperwiki\n",
    "\n",
    "!{pip} install pandas\n",
    "!{pip} install networkx\n",
    "\n",
    "!{pip} install geocoder\n",
    "!{pip} install folium\n",
    "!{pip} install uk-postcode-utils"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Scraping the Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "#Configure name of scraper sqlite database file\n",
    "import os\n",
    "os.environ[\"SCRAPERWIKI_DATABASE_NAME\"] ='sqlite:///{}'.format(dbname)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "# SCRAPER CODE REUSED FROM A LONG TIME AGO, WITH MINOR TWEAKS\n",
    "\n",
    "#code from https://classic.scraperwiki.com/scrapers/iw_poll_notices_scrape/\n",
    "#with a couple of minor tweaks - seach for strings using 'in' rather than 'startwsith'\n",
    "import scraperwiki\n",
    "import requests, lxml.etree\n",
    "\n",
    "#Current local election notice of election PDF for Isle of Wight - looks to be same format-ish as before\n",
    "#url='https://www.iwight.com/azservices/documents/1174-Notice-of-Poll-IOWC-2017.pdf'\n",
    "\n",
    "\n",
    "#Read in the Notice of Poll PDF\n",
    "pdfdata = requests.get(url).content\n",
    "\n",
    "#Convert PDF to XML - this breaks in Python 3?\n",
    "xmldata = scraperwiki.pdftoxml(pdfdata)\n",
    "\n",
    "root = lxml.etree.fromstring(xmldata)\n",
    "pages = list(root)\n",
    "\n",
    "# this function has to work recursively because we might have \"<b>Part1 <i>part 2</i></b>\"\n",
    "def gettext_with_bi_tags(el):\n",
    "    res = [ ]\n",
    "    if el.text:\n",
    "        res.append(el.text)\n",
    "    for lel in el:\n",
    "        res.append(\"<%s>\" % lel.tag)\n",
    "        res.append(gettext_with_bi_tags(lel))\n",
    "        res.append(\"</%s>\" % lel.tag)\n",
    "        if el.tail:\n",
    "            res.append(el.tail)\n",
    "    return \"\".join(res).strip()\n",
    "\n",
    "\n",
    "#Scrape the separate pages\n",
    "#print(pages)\n",
    "for page in pages:\n",
    "    data={'stations':[]}\n",
    "    phase=0\n",
    "    for el in page:\n",
    "        #print(el.attrib, gettext_with_bi_tags(el))\n",
    "        if 'Election of' in gettext_with_bi_tags(el):\n",
    "            phase=1\n",
    "            continue\n",
    "        tmp=gettext_with_bi_tags(el).strip()\n",
    "        if phase==1:\n",
    "            if tmp=='':pass\n",
    "            else:\n",
    "                data['ward']=tmp\n",
    "                phase=phase+1\n",
    "        elif phase==2:\n",
    "            if 'Proposers' in tmp:\n",
    "                phase=3\n",
    "                record={'candidate':[],'address':[],'desc':[],'proposers':[],'seconders':[]}\n",
    "                data['list']=[]\n",
    "                continue\n",
    "        elif phase==3:\n",
    "            if tmp.strip()=='':\n",
    "                phase=4\n",
    "                #print('-------------------------------')\n",
    "                data['list'].append(record)\n",
    "                continue\n",
    "            elif int(el.attrib['left'])<100:\n",
    "                if record['address']!=[]:\n",
    "                    data['list'].append(record)\n",
    "                    record={'candidate':[],'address':[],'desc':[],'proposers':[],'seconders':[]}\n",
    "                record['candidate'].append(tmp)\n",
    "            elif int(el.attrib['left'])<300: record['address'].append(tmp)\n",
    "            elif int(el.attrib['left'])<450: record['desc'].append(tmp)\n",
    "            elif int(el.attrib['left'])<600:\n",
    "                if tmp.startswith('('): record['proposers'][-1]=record['proposers'][-1]+' '+tmp\n",
    "                elif len(record['proposers'])>0 and record['proposers'][-1].strip().endswith('-'): record['proposers'][-1]=record['proposers'][-1]+tmp\n",
    "                elif len(record['proposers'])>0 and record['proposers'][-1].strip().endswith('.'): record['proposers'][-1]=record['proposers'][-1]+' '+tmp\n",
    "                else: record['proposers'].append(tmp)\n",
    "            elif int(el.attrib['left'])<750:\n",
    "                if tmp.startswith('('): record['seconders'][-1]=record['seconders'][-1]+' '+tmp\n",
    "                elif len(record['seconders'])>0 and record['seconders'][-1].strip().endswith('-'): record['seconders'][-1]=record['seconders'][-1]+tmp\n",
    "                elif len(record['seconders'])>0 and record['seconders'][-1].strip().endswith('.'): record['seconders'][-1]=record['seconders'][-1]+' '+tmp\n",
    "                else: record['seconders'].append(tmp)\n",
    "        elif phase==4:\n",
    "            if 'persons entitled to vote' in tmp:\n",
    "                phase=5\n",
    "                record={'station':[],'range':[]}\n",
    "                continue\n",
    "        elif phase==5: #Not implemented... TO DO\n",
    "            #print(el.attrib, gettext_with_bi_tags(el))\n",
    "            if tmp.strip()=='':\n",
    "                data['stations'].append(record)\n",
    "                break #The following bits are broken...\n",
    "            #need to add situation\n",
    "            elif int(el.attrib['left'])<100:\n",
    "                if record['range']!=[]:\n",
    "                    data['stations'].append(record)\n",
    "                    record={'situation':[],'station':[],'range':[]}\n",
    "                record['station'].append(tmp)\n",
    "            elif int(el.attrib['left'])>300:\n",
    "                record['range'].append(tmp)\n",
    "    #print(data)\n",
    "    tmpdata=[]\n",
    "    for station in data['stations']:\n",
    "        tmpdata.append({'ward':data['ward'],\n",
    "                        #'situation':' '.join(station['situation']),\n",
    "                        'station':' '.join(station['station']),\n",
    "                        'range':' '.join(station['range'])})\n",
    "    scraperwiki.sqlite.save(unique_keys=[], table_name='stations', data=tmpdata)\n",
    "    tmpdata=[]\n",
    "    tmpdata2=[]\n",
    "#'desc': ['The Conservative Party', 'Candidate'], 'candidate': ['OULTON', 'Erica'], 'address': ['Blandings, Horringford,', 'Arreton, IW, PO30 3AP']\n",
    "    for candidate in data['list']:\n",
    "        tmpdata.append( {'ward':data['ward'],'candidate':' '.join(candidate['candidate']).encode('ascii','ignore'),\n",
    "                         'address':' '.join(candidate['address']),'desc':' '.join(candidate['desc']) } )\n",
    "        party=' '.join(candidate['desc']).replace('Candidate','').strip()\n",
    "        cand=' '.join(candidate['candidate']).encode('ascii','ignore')\n",
    "        cs=cand.strip(' ').split(' ')\n",
    "        if len(cs)>2:\n",
    "            cand2=cs[:2]\n",
    "            for ci in cs[2:]:\n",
    "                cand2.append(ci[0]+'.')\n",
    "        else: cand2=cs\n",
    "        ctmp=cand2[0]\n",
    "        cand2.remove(ctmp)\n",
    "        cand2.append(ctmp.title())\n",
    "        candi=' '.join(cand2).encode('ascii','ignore')\n",
    "        for proposer in candidate['proposers']:\n",
    "            if proposer.find('(+)')>-1:\n",
    "                proposer=proposer.replace('(+)','').strip()\n",
    "                typ='proposer'\n",
    "            else:typ='assentor'\n",
    "            tmpdata2.append({ 'ward':data['ward'],'candidate':cand, 'candinit':candi, 'support':proposer,'role':'proposal', 'typ':typ, 'desc':party }.copy())\n",
    "        for seconder in candidate['seconders']:\n",
    "            if seconder.find('(++)')>-1:\n",
    "                seconder=seconder.replace('(++)','').strip().encode('ascii','ignore')\n",
    "                typ='seconder'\n",
    "            else:typ='assentor'\n",
    "            tmpdata2.append({ 'ward':data['ward'],'candidate':cand, 'candinit':candi, 'support':seconder,'role':'seconding', 'typ':typ, 'desc':party }.copy())\n",
    "\n",
    "    scraperwiki.sqlite.save(unique_keys=[], table_name='candidates', data=tmpdata)\n",
    "    scraperwiki.sqlite.save(unique_keys=[], table_name='support', data=tmpdata2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{u'candidates': u'CREATE TABLE candidates (\\n\\tward TEXT, \\n\\t\"desc\" TEXT, \\n\\tcandidate TEXT, \\n\\taddress TEXT\\n)',\n",
       " u'stations': u'CREATE TABLE stations (\\n\\tward TEXT, \\n\\tstation TEXT, \\n\\trange TEXT\\n)',\n",
       " u'support': u'CREATE TABLE support (\\n\\tcandinit TEXT, \\n\\trole TEXT, \\n\\tcandidate TEXT, \\n\\tsupport TEXT, \\n\\ttyp TEXT, \\n\\tward TEXT, \\n\\t\"desc\" TEXT\\n)'}"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Check database tables\n",
    "scraperwiki.sql.show_tables()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Querying the Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Users/ajh59/anaconda/lib/python2.7/site-packages/matplotlib/font_manager.py:273: UserWarning: Matplotlib is building the font cache using fc-list. This may take a moment.\n",
      "  warnings.warn('Matplotlib is building the font cache using fc-list. This may take a moment.')\n"
     ]
    }
   ],
   "source": [
    "%matplotlib inline\n",
    "import pandas as pd\n",
    "import sqlite3\n",
    "\n",
    "#Create a connection to the database so we can query it using pandas\n",
    "conn = sqlite3.connect(dbname)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ward</th>\n",
       "      <th>station</th>\n",
       "      <th>range</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Clavering</td>\n",
       "      <td></td>\n",
       "      <td></td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Costessey Methodist Church Hall, Norwich Road,...</td>\n",
       "      <td>18  LU1-1 to LU1-2092</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Costessey - Breckland Hall, Breckland Road, Ne...</td>\n",
       "      <td>19  LV1-1 to LV1-2260</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Costessey - Baptist Church Hall, The Street, O...</td>\n",
       "      <td>20  NE1-1 to NE1-1927</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Costessey Victory Academy, Luke Day Block, Vic...</td>\n",
       "      <td>21  NF1-1 to NF1-2419</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "        ward                                            station  \\\n",
       "0  Clavering                                                      \n",
       "1  Costessey  Costessey Methodist Church Hall, Norwich Road,...   \n",
       "2  Costessey  Costessey - Breckland Hall, Breckland Road, Ne...   \n",
       "3  Costessey  Costessey - Baptist Church Hall, The Street, O...   \n",
       "4  Costessey  Costessey Victory Academy, Luke Day Block, Vic...   \n",
       "\n",
       "                   range  \n",
       "0                         \n",
       "1  18  LU1-1 to LU1-2092  \n",
       "2  19  LV1-1 to LV1-2260  \n",
       "3  20  NE1-1 to NE1-1927  \n",
       "4  21  NF1-1 to NF1-2419  "
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#TO DO... scraper not complete for extracting poll station info\n",
    "stations= pd.read_sql_query(\"SELECT * FROM stations\", conn)\n",
    "stations.head(5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ward</th>\n",
       "      <th>desc</th>\n",
       "      <th>candidate</th>\n",
       "      <th>address</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>BROWN Christopher John</td>\n",
       "      <td>Globe House, Norwich Road, Denton, Harleston, ...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>FOWLER Nicola Jeannette</td>\n",
       "      <td>21 Springfields, Poringland, Norwich, NR14 7RG</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>STONE Margaret Florence</td>\n",
       "      <td>25 Field Lane, Hempnall, Norwich, Norfolk, NR1...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>EAST Tim</td>\n",
       "      <td>7 St Walstans Close, Costessey, Norwich, NR5 0TW</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>GARRARD Jonathan Peter</td>\n",
       "      <td>68 Dereham Road, New Costessey, Norwich, NR5 0SY</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "        ward                desc                candidate  \\\n",
       "0  Clavering    Liberal Democrat   BROWN Christopher John   \n",
       "1  Clavering        Labour Party  FOWLER Nicola Jeannette   \n",
       "2  Clavering  Conservative Party  STONE Margaret Florence   \n",
       "3  Costessey    Liberal Democrat                 EAST Tim   \n",
       "4  Costessey        Labour Party   GARRARD Jonathan Peter   \n",
       "\n",
       "                                             address  \n",
       "0  Globe House, Norwich Road, Denton, Harleston, ...  \n",
       "1     21 Springfields, Poringland, Norwich, NR14 7RG  \n",
       "2  25 Field Lane, Hempnall, Norwich, Norfolk, NR1...  \n",
       "3   7 St Walstans Close, Costessey, Norwich, NR5 0TW  \n",
       "4   68 Dereham Road, New Costessey, Norwich, NR5 0SY  "
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "candidates = pd.read_sql_query(\"SELECT * FROM candidates\", conn)\n",
    "\n",
    "#Clean the data a bit - should maybe do this as part of the scrape, or provide a \"clean col\" as part of scrape\n",
    "candidates['desc']=candidates['desc'].str.replace('The ','').str.replace(' Candidate','')\n",
    "candidates.head(5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([u'BROWN Christopher John', u'FOWLER Nicola Jeannette',\n",
       "       u'STONE Margaret Florence', u'EAST Tim', u'GARRARD Jonathan Peter',\n",
       "       u'ROWETT Catherine Joanna', u'WILTSHIRE Andrew Roy',\n",
       "       u'DAVISON Chris', u'KIDDIE Keith Walter', u'MILTON David',\n",
       "       u'SCOGGINS Tracy Barbara', u'EDDY James William',\n",
       "       u'KUZMIC Susan Evelyn', u'WILBY Martin James',\n",
       "       u'FOULGER Colin Wayne', u'MCCLENNING Robert Arthur',\n",
       "       u'SEWELL Steven Leigh', u'FOWLER Tom', u'HAMMOND Matthew',\n",
       "       u'THOMSON Vic', u'BLATHWAYT Paul Wynter', u'DEWSBURY Margaret',\n",
       "       u'LEMAN James Edward George', u'BILLS David',\n",
       "       u'GULLIVER Bethan Sin', u'SUTTON Jacky', u'BINGHAM David Kenneth',\n",
       "       u'BISSONNET David George', u'STONE Barry Michael', u'KATZ Elana',\n",
       "       u'PERCIVAL Roger Neil', u'THOMAS Alison Mary', u'REEKIE Pam',\n",
       "       u'SPRATT Beverley Herbert Allison', u'SPRATT Ian Victor',\n",
       "       u'HALLS Julian Lawrence', u'MOONEY Joe', u'UNDERWOOD Doug'], dtype=object)"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "candidates['candidate'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "#Save supportes data file\n",
    "candidates.to_csv(candsfilename,index=False)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Geocode and Map the Candidates' Addresses"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "import geocoder\n",
    "def gc(address):\n",
    "    g=geocoder.google(address)\n",
    "    try:\n",
    "        return '{},{}'.format(g.latlng[0],g.latlng[1])\n",
    "    except:\n",
    "        pass\n",
    "    try:\n",
    "        pc=address.split(',')[-1].strip()\n",
    "        if pc.startswith('PO'):\n",
    "            g=geocoder.google(pc)\n",
    "            return '{},{}'.format(g.latlng[0],g.latlng[1])\n",
    "        else: return ''\n",
    "    except:\n",
    "        return ''\n",
    "\n",
    "candidates['latlong']=candidates['address'].apply(gc)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ward</th>\n",
       "      <th>desc</th>\n",
       "      <th>candidate</th>\n",
       "      <th>address</th>\n",
       "      <th>latlong</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>BROWN Christopher John</td>\n",
       "      <td>Globe House, Norwich Road, Denton, Harleston, ...</td>\n",
       "      <td>52.448507,1.35477</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>FOWLER Nicola Jeannette</td>\n",
       "      <td>21 Springfields, Poringland, Norwich, NR14 7RG</td>\n",
       "      <td>52.5693366,1.3469526</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>STONE Margaret Florence</td>\n",
       "      <td>25 Field Lane, Hempnall, Norwich, Norfolk, NR1...</td>\n",
       "      <td>52.4988471,1.298969</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>EAST Tim</td>\n",
       "      <td>7 St Walstans Close, Costessey, Norwich, NR5 0TW</td>\n",
       "      <td>52.6460063,1.2041219</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>GARRARD Jonathan Peter</td>\n",
       "      <td>68 Dereham Road, New Costessey, Norwich, NR5 0SY</td>\n",
       "      <td>52.642241,1.231012</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "        ward                desc                candidate  \\\n",
       "0  Clavering    Liberal Democrat   BROWN Christopher John   \n",
       "1  Clavering        Labour Party  FOWLER Nicola Jeannette   \n",
       "2  Clavering  Conservative Party  STONE Margaret Florence   \n",
       "3  Costessey    Liberal Democrat                 EAST Tim   \n",
       "4  Costessey        Labour Party   GARRARD Jonathan Peter   \n",
       "\n",
       "                                             address               latlong  \n",
       "0  Globe House, Norwich Road, Denton, Harleston, ...     52.448507,1.35477  \n",
       "1     21 Springfields, Poringland, Norwich, NR14 7RG  52.5693366,1.3469526  \n",
       "2  25 Field Lane, Hempnall, Norwich, Norfolk, NR1...   52.4988471,1.298969  \n",
       "3   7 St Walstans Close, Costessey, Norwich, NR5 0TW  52.6460063,1.2041219  \n",
       "4   68 Dereham Road, New Costessey, Norwich, NR5 0SY    52.642241,1.231012  "
      ]
     },
     "execution_count": 21,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "candidates.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "            <div style=\"width:100%;\">\n",
       "            <div style=\"position:relative;width:100%;height:0;padding-bottom:60%;\">\n",
       "            <iframe src=\"data:text/html;base64,CiAgICAgICAgPCFET0NUWVBFIGh0bWw+CiAgICAgICAgPGhlYWQ+CiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgICAgICA8bWV0YSBodHRwLWVxdWl2PSJjb250ZW50LXR5cGUiIGNvbnRlbnQ9InRleHQvaHRtbDsgY2hhcnNldD1VVEYtOCIgLz4KICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2NkbmpzLmNsb3VkZmxhcmUuY29tL2FqYXgvbGlicy9sZWFmbGV0LzAuNy4zL2xlYWZsZXQuanMiPjwvc2NyaXB0PgogICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgPHNjcmlwdCBzcmM9Imh0dHBzOi8vYWpheC5nb29nbGVhcGlzLmNvbS9hamF4L2xpYnMvanF1ZXJ5LzEuMTEuMS9qcXVlcnkubWluLmpzIj48L3NjcmlwdD4KICAgICAgICAKICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIDxzY3JpcHQgc3JjPSJodHRwczovL21heGNkbi5ib290c3RyYXBjZG4uY29tL2Jvb3RzdHJhcC8zLjIuMC9qcy9ib290c3RyYXAubWluLmpzIj48L3NjcmlwdD4KICAgICAgICAKICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIDxzY3JpcHQgc3JjPSJodHRwczovL3Jhd2dpdGh1Yi5jb20vbHZvb2dkdC9MZWFmbGV0LmF3ZXNvbWUtbWFya2Vycy8yLjAvZGV2ZWxvcC9kaXN0L2xlYWZsZXQuYXdlc29tZS1tYXJrZXJzLmpzIj48L3NjcmlwdD4KICAgICAgICAKICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2NkbmpzLmNsb3VkZmxhcmUuY29tL2FqYXgvbGlicy9sZWFmbGV0Lm1hcmtlcmNsdXN0ZXIvMC40LjAvbGVhZmxldC5tYXJrZXJjbHVzdGVyLXNyYy5qcyI+PC9zY3JpcHQ+CiAgICAgICAgCiAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgICAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvbGVhZmxldC5tYXJrZXJjbHVzdGVyLzAuNC4wL2xlYWZsZXQubWFya2VyY2x1c3Rlci5qcyI+PC9zY3JpcHQ+CiAgICAgICAgCiAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgICAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Imh0dHBzOi8vY2RuanMuY2xvdWRmbGFyZS5jb20vYWpheC9saWJzL2xlYWZsZXQvMC43LjMvbGVhZmxldC5jc3MiIC8+CiAgICAgICAgCiAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgICAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Imh0dHBzOi8vbWF4Y2RuLmJvb3RzdHJhcGNkbi5jb20vYm9vdHN0cmFwLzMuMi4wL2Nzcy9ib290c3RyYXAubWluLmNzcyIgLz4KICAgICAgICAKICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9tYXhjZG4uYm9vdHN0cmFwY2RuLmNvbS9ib290c3RyYXAvMy4yLjAvY3NzL2Jvb3RzdHJhcC10aGVtZS5taW4uY3NzIiAvPgogICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL21heGNkbi5ib290c3RyYXBjZG4uY29tL2ZvbnQtYXdlc29tZS80LjEuMC9jc3MvZm9udC1hd2Vzb21lLm1pbi5jc3MiIC8+CiAgICAgICAgCiAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgICAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Imh0dHBzOi8vcmF3Z2l0LmNvbS9sdm9vZ2R0L0xlYWZsZXQuYXdlc29tZS1tYXJrZXJzLzIuMC9kZXZlbG9wL2Rpc3QvbGVhZmxldC5hd2Vzb21lLW1hcmtlcnMuY3NzIiAvPgogICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL2NkbmpzLmNsb3VkZmxhcmUuY29tL2FqYXgvbGlicy9sZWFmbGV0Lm1hcmtlcmNsdXN0ZXIvMC40LjAvTWFya2VyQ2x1c3Rlci5EZWZhdWx0LmNzcyIgLz4KICAgICAgICAKICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvbGVhZmxldC5tYXJrZXJjbHVzdGVyLzAuNC4wL01hcmtlckNsdXN0ZXIuY3NzIiAvPgogICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vcHl0aG9uLXZpc3VhbGl6YXRpb24vZm9saXVtL21hc3Rlci9mb2xpdW0vdGVtcGxhdGVzL2xlYWZsZXQuYXdlc29tZS5yb3RhdGUuY3NzIiAvPgogICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKICAgICAgICAgICAgPHN0eWxlPgoKICAgICAgICAgICAgaHRtbCwgYm9keSB7CiAgICAgICAgICAgICAgICB3aWR0aDogMTAwJTsKICAgICAgICAgICAgICAgIGhlaWdodDogMTAwJTsKICAgICAgICAgICAgICAgIG1hcmdpbjogMDsKICAgICAgICAgICAgICAgIHBhZGRpbmc6IDA7CiAgICAgICAgICAgICAgICB9CgogICAgICAgICAgICAjbWFwIHsKICAgICAgICAgICAgICAgIHBvc2l0aW9uOmFic29sdXRlOwogICAgICAgICAgICAgICAgdG9wOjA7CiAgICAgICAgICAgICAgICBib3R0b206MDsKICAgICAgICAgICAgICAgIHJpZ2h0OjA7CiAgICAgICAgICAgICAgICBsZWZ0OjA7CiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgIDwvc3R5bGU+CiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKICAgICAgICAgICAgPHN0eWxlPiAjbWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiIHsKICAgICAgICAgICAgICAgIHBvc2l0aW9uIDogcmVsYXRpdmU7CiAgICAgICAgICAgICAgICB3aWR0aCA6IDEwMC4wJTsKICAgICAgICAgICAgICAgIGhlaWdodDogMTAwLjAlOwogICAgICAgICAgICAgICAgbGVmdDogMC4wJTsKICAgICAgICAgICAgICAgIHRvcDogMC4wJTsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgPC9zdHlsZT4KICAgICAgICAKICAgICAgICAKICAgICAgICAKICAgICAgICA8L2hlYWQ+CiAgICAgICAgPGJvZHk+CiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKICAgICAgICAgICAgPGRpdiBjbGFzcz0iZm9saXVtLW1hcCIgaWQ9Im1hcF9hZjU1MjUxMjA0NGM0MzViOGQ3ZTkwOTI2ZTcwZTA0YiIgPjwvZGl2PgogICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgIDwvYm9keT4KICAgICAgICA8c2NyaXB0PgogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCgogICAgICAgICAgICB2YXIgc291dGhXZXN0ID0gTC5sYXRMbmcoLTkwLCAtMTgwKTsKICAgICAgICAgICAgdmFyIG5vcnRoRWFzdCA9IEwubGF0TG5nKDkwLCAxODApOwogICAgICAgICAgICB2YXIgYm91bmRzID0gTC5sYXRMbmdCb3VuZHMoc291dGhXZXN0LCBub3J0aEVhc3QpOwoKICAgICAgICAgICAgdmFyIG1hcF9hZjU1MjUxMjA0NGM0MzViOGQ3ZTkwOTI2ZTcwZTA0YiA9IEwubWFwKCdtYXBfYWY1NTI1MTIwNDRjNDM1YjhkN2U5MDkyNmU3MGUwNGInLCB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjZW50ZXI6WzUyLjQ0ODUwNywxLjM1NDc3XSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHpvb206IDExLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgbWF4Qm91bmRzOiBib3VuZHMsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBsYXllcnM6IFtdCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfSk7CiAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgdGlsZV9sYXllcl9lNjg3N2U5YjcyNGM0NWRiODg4MDAwOTkyZTg2OGE4ZSA9IEwudGlsZUxheWVyKAogICAgICAgICAgICAgICAgJ2h0dHBzOi8ve3N9LnRpbGUub3BlbnN0cmVldG1hcC5vcmcve3p9L3t4fS97eX0ucG5nJywKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgICBtYXhab29tOiAxOCwKICAgICAgICAgICAgICAgICAgICBtaW5ab29tOiAxLAogICAgICAgICAgICAgICAgICAgIGF0dHJpYnV0aW9uOiAnTWFwIGRhdGEgKGMpIDxhIGhyZWY9Imh0dHA6Ly9vcGVuc3RyZWV0bWFwLm9yZyI+T3BlblN0cmVldE1hcDwvYT4gY29udHJpYnV0b3JzJywKICAgICAgICAgICAgICAgICAgICBkZXRlY3RSZXRpbmE6IGZhbHNlCiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgKS5hZGRUbyhtYXBfYWY1NTI1MTIwNDRjNDM1YjhkN2U5MDkyNmU3MGUwNGIpOwoKICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCgogICAgICAgICAgICB2YXIgbWFya2VyX2RjNTNiZDVlZDRlYjQ4YTI5NDZlYzQ0M2I5YzE2ZDY4ID0gTC5tYXJrZXIoCiAgICAgICAgICAgICAgICBbNTIuNDQ4NTA3LDEuMzU0NzddLAogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAgIGljb246IG5ldyBMLkljb24uRGVmYXVsdCgpCiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF9hZjU1MjUxMjA0NGM0MzViOGQ3ZTkwOTI2ZTcwZTA0Yik7CiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKICAgICAgICAgICAgdmFyIHBvcHVwXzg1NDM0MjJlNjcxMzQwYzU5OThiZGY0NDk3MjZjMzVjID0gTC5wb3B1cCh7bWF4V2lkdGg6ICczMDAnfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sX2NjMzczMzllZTE4NzQ1ZWM4NDkwNWE4MzdjYzNlYmUzID0gJCgnICAgICAgICAgPGRpdiBpZD0iaHRtbF9jYzM3MzM5ZWUxODc0NWVjODQ5MDVhODM3Y2MzZWJlMyIgICAgICAgICAgICAgICAgIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPiAgICAgICAgICAgICAgICAgQlJPV04gQ2hyaXN0b3BoZXIgSm9obiwgKExpYmVyYWwgRGVtb2NyYXQpIENsYXZlcmluZzwvZGl2PiAgICAgICAgICAgICAgICAgJylbMF07CiAgICAgICAgICAgICAgICBwb3B1cF84NTQzNDIyZTY3MTM0MGM1OTk4YmRmNDQ5NzI2YzM1Yy5zZXRDb250ZW50KGh0bWxfY2MzNzMzOWVlMTg3NDVlYzg0OTA1YTgzN2NjM2ViZTMpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIG1hcmtlcl9kYzUzYmQ1ZWQ0ZWI0OGEyOTQ2ZWM0NDNiOWMxNmQ2OC5iaW5kUG9wdXAocG9wdXBfODU0MzQyMmU2NzEzNDBjNTk5OGJkZjQ0OTcyNmMzNWMpOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAoKICAgICAgICAgICAgdmFyIG1hcmtlcl9hMTkwYzg0ZGI1NGU0OWU4YWI4ZWE5ODVhNThlM2E4NyA9IEwubWFya2VyKAogICAgICAgICAgICAgICAgWzUyLjU2OTMzNjYsMS4zNDY5NTI2XSwKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgICBpY29uOiBuZXcgTC5JY29uLkRlZmF1bHQoKQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfYWY1NTI1MTIwNDRjNDM1YjhkN2U5MDkyNmU3MGUwNGIpOwogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgICAgIHZhciBwb3B1cF8zNjk3ODU1MDQ2ZGQ0YTliYTk1NTE1MmIwZjE2M2FmMCA9IEwucG9wdXAoe21heFdpZHRoOiAnMzAwJ30pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF8yMmU3NzZlOWM0MDE0NDkwYTg5ODMyYjc5YmJlYTVmNyA9ICQoJyAgICAgICAgIDxkaXYgaWQ9Imh0bWxfMjJlNzc2ZTljNDAxNDQ5MGE4OTgzMmI3OWJiZWE1ZjciICAgICAgICAgICAgICAgICBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij4gICAgICAgICAgICAgICAgIEZPV0xFUiBOaWNvbGEgSmVhbm5ldHRlLCAoTGFib3VyIFBhcnR5KSBDbGF2ZXJpbmc8L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfMzY5Nzg1NTA0NmRkNGE5YmE5NTUxNTJiMGYxNjNhZjAuc2V0Q29udGVudChodG1sXzIyZTc3NmU5YzQwMTQ0OTBhODk4MzJiNzliYmVhNWY3KTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfYTE5MGM4NGRiNTRlNDllOGFiOGVhOTg1YTU4ZTNhODcuYmluZFBvcHVwKHBvcHVwXzM2OTc4NTUwNDZkZDRhOWJhOTU1MTUyYjBmMTYzYWYwKTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfMzY3MzBkYTZjNTcxNDNjMzk4OTgxYzVmMWIyMTMyMWIgPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi40OTg4NDcxLDEuMjk4OTY5XSwKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgICBpY29uOiBuZXcgTC5JY29uLkRlZmF1bHQoKQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfYWY1NTI1MTIwNDRjNDM1YjhkN2U5MDkyNmU3MGUwNGIpOwogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgICAgIHZhciBwb3B1cF9kNzBlYTUxZGU2M2I0OTA1ODkwNjVlYmNmZGFhNDU1MiA9IEwucG9wdXAoe21heFdpZHRoOiAnMzAwJ30pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF9iNjZiNDc3ODFmMzI0NWVlYTg3NTg3ODg3NzkxMjllYyA9ICQoJyAgICAgICAgIDxkaXYgaWQ9Imh0bWxfYjY2YjQ3NzgxZjMyNDVlZWE4NzU4Nzg4Nzc5MTI5ZWMiICAgICAgICAgICAgICAgICBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij4gICAgICAgICAgICAgICAgIFNUT05FIE1hcmdhcmV0IEZsb3JlbmNlLCAoQ29uc2VydmF0aXZlIFBhcnR5KSBDbGF2ZXJpbmc8L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfZDcwZWE1MWRlNjNiNDkwNTg5MDY1ZWJjZmRhYTQ1NTIuc2V0Q29udGVudChodG1sX2I2NmI0Nzc4MWYzMjQ1ZWVhODc1ODc4ODc3OTEyOWVjKTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfMzY3MzBkYTZjNTcxNDNjMzk4OTgxYzVmMWIyMTMyMWIuYmluZFBvcHVwKHBvcHVwX2Q3MGVhNTFkZTYzYjQ5MDU4OTA2NWViY2ZkYWE0NTUyKTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfZmM1NDMxZmYzMTkyNGQwM2FkNDExZjQ2OTViMDAzYTkgPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi42NDYwMDYzLDEuMjA0MTIxOV0sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfNjA1MzZlMTc4MmFjNGJjNDljNGQ4MjVkOGRhYmNjZGEgPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfMmFlZDZlZmZmYTI1NDZiZTk4ZWNmMGJjNWYzN2I0OTQgPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sXzJhZWQ2ZWZmZmEyNTQ2YmU5OGVjZjBiYzVmMzdiNDk0IiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBFQVNUIFRpbSwgKExpYmVyYWwgRGVtb2NyYXQpIENvc3Rlc3NleTwvZGl2PiAgICAgICAgICAgICAgICAgJylbMF07CiAgICAgICAgICAgICAgICBwb3B1cF82MDUzNmUxNzgyYWM0YmM0OWM0ZDgyNWQ4ZGFiY2NkYS5zZXRDb250ZW50KGh0bWxfMmFlZDZlZmZmYTI1NDZiZTk4ZWNmMGJjNWYzN2I0OTQpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIG1hcmtlcl9mYzU0MzFmZjMxOTI0ZDAzYWQ0MTFmNDY5NWIwMDNhOS5iaW5kUG9wdXAocG9wdXBfNjA1MzZlMTc4MmFjNGJjNDljNGQ4MjVkOGRhYmNjZGEpOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAoKICAgICAgICAgICAgdmFyIG1hcmtlcl85OWIwODRmYmI2NjU0ZDdiYWMzNDA3MzNmMmRiZDI3YiA9IEwubWFya2VyKAogICAgICAgICAgICAgICAgWzUyLjY0MjI0MSwxLjIzMTAxMl0sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfOGU0ZjUyYTBiYjA0NGM1NzllZDEyYzM1NTI5MGQ4NTYgPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfNjlhMzIyMTEwNzc0NDJjNTg5NTY3MmRjOTg4YjYzZTggPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sXzY5YTMyMjExMDc3NDQyYzU4OTU2NzJkYzk4OGI2M2U4IiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBHQVJSQVJEIEpvbmF0aGFuIFBldGVyLCAoTGFib3VyIFBhcnR5KSBDb3N0ZXNzZXk8L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfOGU0ZjUyYTBiYjA0NGM1NzllZDEyYzM1NTI5MGQ4NTYuc2V0Q29udGVudChodG1sXzY5YTMyMjExMDc3NDQyYzU4OTU2NzJkYzk4OGI2M2U4KTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfOTliMDg0ZmJiNjY1NGQ3YmFjMzQwNzMzZjJkYmQyN2IuYmluZFBvcHVwKHBvcHVwXzhlNGY1MmEwYmIwNDRjNTc5ZWQxMmMzNTUyOTBkODU2KTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfNmExYTU3MTk5ZTcyNDQ1MWFlMWY3MDgzNWU1ZWNkYzYgPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi42MjE0ODc2LDEuMjYyODkyNV0sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfNGEzZDZhMjVmYTkyNDQ3MzhlYjE1YmQwYWNjMjMwZDQgPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfNTI0MDQ1NTAzN2U2NDFjZWEzNjIyN2Y4MGU0ZjU5MTUgPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sXzUyNDA0NTUwMzdlNjQxY2VhMzYyMjdmODBlNGY1OTE1IiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBST1dFVFQgQ2F0aGVyaW5lIEpvYW5uYSwgKEdyZWVuIFBhcnR5KSBDb3N0ZXNzZXk8L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfNGEzZDZhMjVmYTkyNDQ3MzhlYjE1YmQwYWNjMjMwZDQuc2V0Q29udGVudChodG1sXzUyNDA0NTUwMzdlNjQxY2VhMzYyMjdmODBlNGY1OTE1KTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfNmExYTU3MTk5ZTcyNDQ1MWFlMWY3MDgzNWU1ZWNkYzYuYmluZFBvcHVwKHBvcHVwXzRhM2Q2YTI1ZmE5MjQ0NzM4ZWIxNWJkMGFjYzIzMGQ0KTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfMmRhZjNkODliN2YwNGRkYWJkNDkyM2FlMzQ0MDQ1ZWIgPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi42NTQxMTgsMS4xNjIwODg3XSwKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgICBpY29uOiBuZXcgTC5JY29uLkRlZmF1bHQoKQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfYWY1NTI1MTIwNDRjNDM1YjhkN2U5MDkyNmU3MGUwNGIpOwogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgICAgIHZhciBwb3B1cF9hMTllNWJmOTk2MTY0N2JmOGU1ZTI5ZTA3YmIyYzI2NyA9IEwucG9wdXAoe21heFdpZHRoOiAnMzAwJ30pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF9jYzQ4Y2VhYzdjODY0NGFhYjIxMGU4M2FlZDg1YWQ1YSA9ICQoJyAgICAgICAgIDxkaXYgaWQ9Imh0bWxfY2M0OGNlYWM3Yzg2NDRhYWIyMTBlODNhZWQ4NWFkNWEiICAgICAgICAgICAgICAgICBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij4gICAgICAgICAgICAgICAgIFdJTFRTSElSRSBBbmRyZXcgUm95LCAoQ29uc2VydmF0aXZlIFBhcnR5KSBDb3N0ZXNzZXk8L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfYTE5ZTViZjk5NjE2NDdiZjhlNWUyOWUwN2JiMmMyNjcuc2V0Q29udGVudChodG1sX2NjNDhjZWFjN2M4NjQ0YWFiMjEwZTgzYWVkODVhZDVhKTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfMmRhZjNkODliN2YwNGRkYWJkNDkyM2FlMzQ0MDQ1ZWIuYmluZFBvcHVwKHBvcHVwX2ExOWU1YmY5OTYxNjQ3YmY4ZTVlMjllMDdiYjJjMjY3KTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfMWY0Yzc1ZmE3YzRmNGZhMmJmMWY5NDExNzBhZDIxZjAgPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi4zNzg4NzIyLDEuMTE2MjE4Ml0sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfNTE3ZjZmMmQyYWVjNDQ1YWE1ZGVkNGQ3ODZiZTYzMGYgPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfYWQ5OTY5NWMyOTNiNGZhZDg4ZDY3NjFiZmE5MjYzZDAgPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sX2FkOTk2OTVjMjkzYjRmYWQ4OGQ2NzYxYmZhOTI2M2QwIiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBEQVZJU09OIENocmlzLCAoTGFib3VyIFBhcnR5KSBEaXNzIGFuZCBSb3lkb248L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfNTE3ZjZmMmQyYWVjNDQ1YWE1ZGVkNGQ3ODZiZTYzMGYuc2V0Q29udGVudChodG1sX2FkOTk2OTVjMjkzYjRmYWQ4OGQ2NzYxYmZhOTI2M2QwKTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfMWY0Yzc1ZmE3YzRmNGZhMmJmMWY5NDExNzBhZDIxZjAuYmluZFBvcHVwKHBvcHVwXzUxN2Y2ZjJkMmFlYzQ0NWFhNWRlZDRkNzg2YmU2MzBmKTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfZGE2ZDMzOTY0ODI5NGIzOTkzMzFmYmIyYTQ5NjYzZGEgPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi4zODEyNjcyLDEuMTEzNjI3OF0sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfZjM4NDc4Nzg5NzEyNDE1ZmI0MDk4NWZkMGNkY2NlNWIgPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfY2Q4ODNhOTEwMDVmNDRiMTgzYzVjNjMxM2EzYzFmZTAgPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sX2NkODgzYTkxMDA1ZjQ0YjE4M2M1YzYzMTNhM2MxZmUwIiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBLSURESUUgS2VpdGggV2FsdGVyLCAoQ29uc2VydmF0aXZlIFBhcnR5KSBEaXNzIGFuZCBSb3lkb248L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfZjM4NDc4Nzg5NzEyNDE1ZmI0MDk4NWZkMGNkY2NlNWIuc2V0Q29udGVudChodG1sX2NkODgzYTkxMDA1ZjQ0YjE4M2M1YzYzMTNhM2MxZmUwKTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfZGE2ZDMzOTY0ODI5NGIzOTkzMzFmYmIyYTQ5NjYzZGEuYmluZFBvcHVwKHBvcHVwX2YzODQ3ODc4OTcxMjQxNWZiNDA5ODVmZDBjZGNjZTViKTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfZjFiNDJhMTE3MzVmNDdlNWJiZjU2ZWIxZjA5ZmE5ZTYgPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi42MzI2NDI0LDEuMjk2MTM0MV0sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfMGEwMmM4YzZlZjFhNDMxZThjODEyYzk2Y2VjN2Y3ZWQgPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfNzQ4NWViOWI1NjBmNDVmYjgzYWFlMjE2ZDdhNjA1ZGUgPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sXzc0ODVlYjliNTYwZjQ1ZmI4M2FhZTIxNmQ3YTYwNWRlIiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBNSUxUT04gRGF2aWQsIChHcmVlbiBQYXJ0eSkgRGlzcyBhbmQgUm95ZG9uPC9kaXY+ICAgICAgICAgICAgICAgICAnKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwXzBhMDJjOGM2ZWYxYTQzMWU4YzgxMmM5NmNlYzdmN2VkLnNldENvbnRlbnQoaHRtbF83NDg1ZWI5YjU2MGY0NWZiODNhYWUyMTZkN2E2MDVkZSk7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgbWFya2VyX2YxYjQyYTExNzM1ZjQ3ZTViYmY1NmViMWYwOWZhOWU2LmJpbmRQb3B1cChwb3B1cF8wYTAyYzhjNmVmMWE0MzFlOGM4MTJjOTZjZWM3ZjdlZCk7CgogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCgogICAgICAgICAgICB2YXIgbWFya2VyXzcxYjE4MDI1MTkwYzQyMjhiMmMwMWJiMDRlZGQ1ZWFlID0gTC5tYXJrZXIoCiAgICAgICAgICAgICAgICBbNTIuNDA3Nzc1MywxLjMwMDcwOF0sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfNzY4Mjc2NDljNzJlNGY1YjhlZjIwZjJjMDNmNWZjYzQgPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfZTg4NjRhOTc4OTdlNGYyODk4Y2RmNGM0ODMwNTIwNGQgPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sX2U4ODY0YTk3ODk3ZTRmMjg5OGNkZjRjNDgzMDUyMDRkIiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBLVVpNSUMgU3VzYW4gRXZlbHluLCAoTGliZXJhbCBEZW1vY3JhdCkgRWFzdCBEZXB3YWRlPC9kaXY+ICAgICAgICAgICAgICAgICAnKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwXzc2ODI3NjQ5YzcyZTRmNWI4ZWYyMGYyYzAzZjVmY2M0LnNldENvbnRlbnQoaHRtbF9lODg2NGE5Nzg5N2U0ZjI4OThjZGY0YzQ4MzA1MjA0ZCk7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgbWFya2VyXzcxYjE4MDI1MTkwYzQyMjhiMmMwMWJiMDRlZGQ1ZWFlLmJpbmRQb3B1cChwb3B1cF83NjgyNzY0OWM3MmU0ZjViOGVmMjBmMmMwM2Y1ZmNjNCk7CgogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCgogICAgICAgICAgICB2YXIgbWFya2VyX2E3NDQzZTFhOGQ0ZTRhMDdhMjk1OThkZWRlNmU5NzRiID0gTC5tYXJrZXIoCiAgICAgICAgICAgICAgICBbNTIuNTY5MzM2NiwxLjM0Njk1MjZdLAogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAgIGljb246IG5ldyBMLkljb24uRGVmYXVsdCgpCiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF9hZjU1MjUxMjA0NGM0MzViOGQ3ZTkwOTI2ZTcwZTA0Yik7CiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKICAgICAgICAgICAgdmFyIHBvcHVwX2RhOGNjNTA4NGIxYzQwOGZhM2Y5NGU5NTQ4ZmYxMmFkID0gTC5wb3B1cCh7bWF4V2lkdGg6ICczMDAnfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sXzc2MDQyYTBjZTg1ZDQ5NDM4ZWZlYjQ4YWMwNzRmOGUzID0gJCgnICAgICAgICAgPGRpdiBpZD0iaHRtbF83NjA0MmEwY2U4NWQ0OTQzOGVmZWI0OGFjMDc0ZjhlMyIgICAgICAgICAgICAgICAgIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPiAgICAgICAgICAgICAgICAgRk9XTEVSIFRvbSwgKExhYm91ciBQYXJ0eSkgSGVuc3RlYWQ8L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfZGE4Y2M1MDg0YjFjNDA4ZmEzZjk0ZTk1NDhmZjEyYWQuc2V0Q29udGVudChodG1sXzc2MDQyYTBjZTg1ZDQ5NDM4ZWZlYjQ4YWMwNzRmOGUzKTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfYTc0NDNlMWE4ZDRlNGEwN2EyOTU5OGRlZGU2ZTk3NGIuYmluZFBvcHVwKHBvcHVwX2RhOGNjNTA4NGIxYzQwOGZhM2Y5NGU5NTQ4ZmYxMmFkKTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfODk4YTQ1ZDRmMzVlNDVkYTg4YjZiYzRmYzgyMTIxMjIgPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi41NzMzNTUzLDEuMzU2ODg3OF0sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfZmZjMDRjNTQzM2JjNGNhZDk2ODBiZTQ0ZmZmZGU5YTggPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfMmQzNTdkMmZmOTRiNDk4NTg4Zjg4ZmZlODFlMWQ3MGMgPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sXzJkMzU3ZDJmZjk0YjQ5ODU4OGY4OGZmZTgxZTFkNzBjIiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBUSE9NU09OIFZpYywgKENvbnNlcnZhdGl2ZSBQYXJ0eSkgSGVuc3RlYWQ8L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfZmZjMDRjNTQzM2JjNGNhZDk2ODBiZTQ0ZmZmZGU5YTguc2V0Q29udGVudChodG1sXzJkMzU3ZDJmZjk0YjQ5ODU4OGY4OGZmZTgxZTFkNzBjKTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfODk4YTQ1ZDRmMzVlNDVkYTg4YjZiYzRmYzgyMTIxMjIuYmluZFBvcHVwKHBvcHVwX2ZmYzA0YzU0MzNiYzRjYWQ5NjgwYmU0NGZmZmRlOWE4KTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfYTdlOTdlZDllYTAwNDEyOGIyYzBjMDY4OTRmYzhlMzggPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi42MjUwNTMzLDEuMTIzODQ3NF0sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfNDM0ZDFhNGNiMzRhNGU1YzllZjc0M2EzZmI1YTNmZTcgPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfZDMyNjdmOGNhYzdiNDM1MTkxN2E3OGRhMjUwNWI3YjkgPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sX2QzMjY3ZjhjYWM3YjQzNTE5MTdhNzhkYTI1MDViN2I5IiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBERVdTQlVSWSBNYXJnYXJldCwgKENvbnNlcnZhdGl2ZSBQYXJ0eSkgSGluZ2hhbTwvZGl2PiAgICAgICAgICAgICAgICAgJylbMF07CiAgICAgICAgICAgICAgICBwb3B1cF80MzRkMWE0Y2IzNGE0ZTVjOWVmNzQzYTNmYjVhM2ZlNy5zZXRDb250ZW50KGh0bWxfZDMyNjdmOGNhYzdiNDM1MTkxN2E3OGRhMjUwNWI3YjkpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIG1hcmtlcl9hN2U5N2VkOWVhMDA0MTI4YjJjMGMwNjg5NGZjOGUzOC5iaW5kUG9wdXAocG9wdXBfNDM0ZDFhNGNiMzRhNGU1YzllZjc0M2EzZmI1YTNmZTcpOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAoKICAgICAgICAgICAgdmFyIG1hcmtlcl80ZTQxNmQ5ODM4OTM0NzU1YWIwMGVkZGRjNzZkNzU1NiA9IEwubWFya2VyKAogICAgICAgICAgICAgICAgWzUyLjU1OTc3NjgsMS4xMjAyNTU3XSwKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgICBpY29uOiBuZXcgTC5JY29uLkRlZmF1bHQoKQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfYWY1NTI1MTIwNDRjNDM1YjhkN2U5MDkyNmU3MGUwNGIpOwogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgICAgIHZhciBwb3B1cF8xZDg0OGI0NGQ5ZTA0NTFkOTgwMTY0ZmJkMDY1YzEyYyA9IEwucG9wdXAoe21heFdpZHRoOiAnMzAwJ30pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF83OWNhOTkzZTQzMjk0MGE5YTJkNzZkZTdjNDVhYTQyNyA9ICQoJyAgICAgICAgIDxkaXYgaWQ9Imh0bWxfNzljYTk5M2U0MzI5NDBhOWEyZDc2ZGU3YzQ1YWE0MjciICAgICAgICAgICAgICAgICBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij4gICAgICAgICAgICAgICAgIExFTUFOIEphbWVzIEVkd2FyZCBHZW9yZ2UsIChMYWJvdXIgUGFydHkpIEhpbmdoYW08L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfMWQ4NDhiNDRkOWUwNDUxZDk4MDE2NGZiZDA2NWMxMmMuc2V0Q29udGVudChodG1sXzc5Y2E5OTNlNDMyOTQwYTlhMmQ3NmRlN2M0NWFhNDI3KTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfNGU0MTZkOTgzODkzNDc1NWFiMDBlZGRkYzc2ZDc1NTYuYmluZFBvcHVwKHBvcHVwXzFkODQ4YjQ0ZDllMDQ1MWQ5ODAxNjRmYmQwNjVjMTJjKTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfMjk5NTAzOWVlNjc2NDAwZDllMjQwZGY4NWIyY2NhN2EgPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi41OTc4NTUsMS4xODE3NDY2XSwKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgICBpY29uOiBuZXcgTC5JY29uLkRlZmF1bHQoKQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfYWY1NTI1MTIwNDRjNDM1YjhkN2U5MDkyNmU3MGUwNGIpOwogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgICAgIHZhciBwb3B1cF9iZWYzMWQ1OTM0Yjk0MGM1YjFlMjIwNzYzNTgzZTVmNCA9IEwucG9wdXAoe21heFdpZHRoOiAnMzAwJ30pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF8zZmE4NGFjMjhkODM0MjI1YWQ0MGZjM2NiNThmMzgwZSA9ICQoJyAgICAgICAgIDxkaXYgaWQ9Imh0bWxfM2ZhODRhYzI4ZDgzNDIyNWFkNDBmYzNjYjU4ZjM4MGUiICAgICAgICAgICAgICAgICBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij4gICAgICAgICAgICAgICAgIEJJTExTIERhdmlkLCAoQ29uc2VydmF0aXZlIFBhcnR5KSBIdW1ibGV5YXJkPC9kaXY+ICAgICAgICAgICAgICAgICAnKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwX2JlZjMxZDU5MzRiOTQwYzViMWUyMjA3NjM1ODNlNWY0LnNldENvbnRlbnQoaHRtbF8zZmE4NGFjMjhkODM0MjI1YWQ0MGZjM2NiNThmMzgwZSk7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgbWFya2VyXzI5OTUwMzllZTY3NjQwMGQ5ZTI0MGRmODViMmNjYTdhLmJpbmRQb3B1cChwb3B1cF9iZWYzMWQ1OTM0Yjk0MGM1YjFlMjIwNzYzNTgzZTVmNCk7CgogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCgogICAgICAgICAgICB2YXIgbWFya2VyXzQ1OTdjYzRkMDQzZDQ5ODliMTc0ZGU1MWIzZDExZTc3ID0gTC5tYXJrZXIoCiAgICAgICAgICAgICAgICBbNTIuNTA3NDYzMSwxLjE1Njc5NTNdLAogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAgIGljb246IG5ldyBMLkljb24uRGVmYXVsdCgpCiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF9hZjU1MjUxMjA0NGM0MzViOGQ3ZTkwOTI2ZTcwZTA0Yik7CiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKICAgICAgICAgICAgdmFyIHBvcHVwXzMwMmM5Y2U1YTgwZDQ2ZTU4OTJiMGUyYmZiNDFlYTAxID0gTC5wb3B1cCh7bWF4V2lkdGg6ICczMDAnfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sXzkyMmRkZTJmZmUyODRmYjhiNzNmNDM0ZWEyOWE5YTc3ID0gJCgnICAgICAgICAgPGRpdiBpZD0iaHRtbF85MjJkZGUyZmZlMjg0ZmI4YjczZjQzNGVhMjlhOWE3NyIgICAgICAgICAgICAgICAgIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPiAgICAgICAgICAgICAgICAgR1VMTElWRVIgQmV0aGFuIFNpbiwgKExhYm91ciBQYXJ0eSkgSHVtYmxleWFyZDwvZGl2PiAgICAgICAgICAgICAgICAgJylbMF07CiAgICAgICAgICAgICAgICBwb3B1cF8zMDJjOWNlNWE4MGQ0NmU1ODkyYjBlMmJmYjQxZWEwMS5zZXRDb250ZW50KGh0bWxfOTIyZGRlMmZmZTI4NGZiOGI3M2Y0MzRlYTI5YTlhNzcpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIG1hcmtlcl80NTk3Y2M0ZDA0M2Q0OTg5YjE3NGRlNTFiM2QxMWU3Ny5iaW5kUG9wdXAocG9wdXBfMzAyYzljZTVhODBkNDZlNTg5MmIwZTJiZmI0MWVhMDEpOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAoKICAgICAgICAgICAgdmFyIG1hcmtlcl8xYTFkMjZhZDQ5NzA0M2YwODIxM2EwYjU1Y2Y3MDIxOSA9IEwubWFya2VyKAogICAgICAgICAgICAgICAgWzUyLjYwMDI2NDQsMS4xNjYxMjk1XSwKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgICBpY29uOiBuZXcgTC5JY29uLkRlZmF1bHQoKQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfYWY1NTI1MTIwNDRjNDM1YjhkN2U5MDkyNmU3MGUwNGIpOwogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgICAgIHZhciBwb3B1cF8xZjlhNTgyNWU2YjU0OWE3YjFlOWE2MGNiNjlmZDhhYSA9IEwucG9wdXAoe21heFdpZHRoOiAnMzAwJ30pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF8yZTk5YjZhYmQ2YjY0OGE3ODNlNzc2MzQxMjIyMTU2NyA9ICQoJyAgICAgICAgIDxkaXYgaWQ9Imh0bWxfMmU5OWI2YWJkNmI2NDhhNzgzZTc3NjM0MTIyMjE1NjciICAgICAgICAgICAgICAgICBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij4gICAgICAgICAgICAgICAgIFNVVFRPTiBKYWNreSwgKExpYmVyYWwgRGVtb2NyYXQpIEh1bWJsZXlhcmQ8L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfMWY5YTU4MjVlNmI1NDlhN2IxZTlhNjBjYjY5ZmQ4YWEuc2V0Q29udGVudChodG1sXzJlOTliNmFiZDZiNjQ4YTc4M2U3NzYzNDEyMjIxNTY3KTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfMWExZDI2YWQ0OTcwNDNmMDgyMTNhMGI1NWNmNzAyMTkuYmluZFBvcHVwKHBvcHVwXzFmOWE1ODI1ZTZiNTQ5YTdiMWU5YTYwY2I2OWZkOGFhKTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfNmJkZTJkYWE5MzM2NGY4MGJkODY3ZTlkMGVjZjY2OGIgPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi41MjA0MDAyLDEuNTA5NTcxM10sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfNWE2MDFmMmMwOWM1NGMyNjhmOTJjOGU5NjIyZTRkNDUgPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfZWE5YjA0ZjdkYTE5NDk0Njk5MmNlNGY0YTE3MWFkOTUgPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sX2VhOWIwNGY3ZGExOTQ5NDY5OTJjZTRmNGExNzFhZDk1IiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBCSU5HSEFNIERhdmlkIEtlbm5ldGgsIChMaWJlcmFsIERlbW9jcmF0KSBMb2Rkb248L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfNWE2MDFmMmMwOWM1NGMyNjhmOTJjOGU5NjIyZTRkNDUuc2V0Q29udGVudChodG1sX2VhOWIwNGY3ZGExOTQ5NDY5OTJjZTRmNGExNzFhZDk1KTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfNmJkZTJkYWE5MzM2NGY4MGJkODY3ZTlkMGVjZjY2OGIuYmluZFBvcHVwKHBvcHVwXzVhNjAxZjJjMDljNTRjMjY4ZjkyYzhlOTYyMmU0ZDQ1KTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfNzY4YWJiZmQ3ZWZlNGE5NGFhNTZmODI5YTE3ODMxNjIgPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi41NzY0NDM2LDEuNDYzNjM0XSwKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgICBpY29uOiBuZXcgTC5JY29uLkRlZmF1bHQoKQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfYWY1NTI1MTIwNDRjNDM1YjhkN2U5MDkyNmU3MGUwNGIpOwogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgICAgIHZhciBwb3B1cF81Zjk5NzA2NzY2ODE0MmE0OGNkNzEwMDRmOGNkNzQ3MiA9IEwucG9wdXAoe21heFdpZHRoOiAnMzAwJ30pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF9mZmY0ZDMyODY3ZTI0YjUyYWEwMDBkNmQxMmEyYjQ3OSA9ICQoJyAgICAgICAgIDxkaXYgaWQ9Imh0bWxfZmZmNGQzMjg2N2UyNGI1MmFhMDAwZDZkMTJhMmI0NzkiICAgICAgICAgICAgICAgICBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij4gICAgICAgICAgICAgICAgIEJJU1NPTk5FVCBEYXZpZCBHZW9yZ2UsIChMYWJvdXIgUGFydHkpIExvZGRvbjwvZGl2PiAgICAgICAgICAgICAgICAgJylbMF07CiAgICAgICAgICAgICAgICBwb3B1cF81Zjk5NzA2NzY2ODE0MmE0OGNkNzEwMDRmOGNkNzQ3Mi5zZXRDb250ZW50KGh0bWxfZmZmNGQzMjg2N2UyNGI1MmFhMDAwZDZkMTJhMmI0NzkpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIG1hcmtlcl83NjhhYmJmZDdlZmU0YTk0YWE1NmY4MjlhMTc4MzE2Mi5iaW5kUG9wdXAocG9wdXBfNWY5OTcwNjc2NjgxNDJhNDhjZDcxMDA0ZjhjZDc0NzIpOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAoKICAgICAgICAgICAgdmFyIG1hcmtlcl9hOTU5MWQ5MDg1NDc0NjMzOGM4ZGU1NzQyMTk2ZGYwZSA9IEwubWFya2VyKAogICAgICAgICAgICAgICAgWzUyLjQ5ODg0NzEsMS4yOTg5NjldLAogICAgICAgICAgICAgICAgewogICAgICAgICAgICAgICAgICAgIGljb246IG5ldyBMLkljb24uRGVmYXVsdCgpCiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgKQogICAgICAgICAgICAgICAgLmFkZFRvKG1hcF9hZjU1MjUxMjA0NGM0MzViOGQ3ZTkwOTI2ZTcwZTA0Yik7CiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKICAgICAgICAgICAgdmFyIHBvcHVwXzMxNWE2NWVhMTYwZTRmZWU4YTJlMjYzMDVjY2UyZjkwID0gTC5wb3B1cCh7bWF4V2lkdGg6ICczMDAnfSk7CgogICAgICAgICAgICAKICAgICAgICAgICAgICAgIHZhciBodG1sXzBhNDZhMTlmODFlMTRlZjE5MTg1NmVjYWNiMzA0MzlmID0gJCgnICAgICAgICAgPGRpdiBpZD0iaHRtbF8wYTQ2YTE5ZjgxZTE0ZWYxOTE4NTZlY2FjYjMwNDM5ZiIgICAgICAgICAgICAgICAgIHN0eWxlPSJ3aWR0aDogMTAwLjAlOyBoZWlnaHQ6IDEwMC4wJTsiPiAgICAgICAgICAgICAgICAgU1RPTkUgQmFycnkgTWljaGFlbCwgKENvbnNlcnZhdGl2ZSBQYXJ0eSkgTG9kZG9uPC9kaXY+ICAgICAgICAgICAgICAgICAnKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwXzMxNWE2NWVhMTYwZTRmZWU4YTJlMjYzMDVjY2UyZjkwLnNldENvbnRlbnQoaHRtbF8wYTQ2YTE5ZjgxZTE0ZWYxOTE4NTZlY2FjYjMwNDM5Zik7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgbWFya2VyX2E5NTkxZDkwODU0NzQ2MzM4YzhkZTU3NDIxOTZkZjBlLmJpbmRQb3B1cChwb3B1cF8zMTVhNjVlYTE2MGU0ZmVlOGEyZTI2MzA1Y2NlMmY5MCk7CgogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCgogICAgICAgICAgICB2YXIgbWFya2VyXzE4YWU0ODczOGFmMjRkMjA4NzBlZGIyODJhNjg4MDczID0gTC5tYXJrZXIoCiAgICAgICAgICAgICAgICBbNTIuNTMzNDk1MSwxLjE1OTk3Nl0sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfNjRhZTk1MDAwMmQ0NDUxMjk1OWFhZmExYWI3ZGQ5ODQgPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfYTFmOTBmNjhmMmFjNDY0ZjhjNmE0OTczYjY5NDNhMzQgPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sX2ExZjkwZjY4ZjJhYzQ2NGY4YzZhNDk3M2I2OTQzYTM0IiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBTUFJBVFQgSWFuIFZpY3RvciwgKExpYmVyYWwgRGVtb2NyYXQpIFdlc3QgRGVwd2FkZTwvZGl2PiAgICAgICAgICAgICAgICAgJylbMF07CiAgICAgICAgICAgICAgICBwb3B1cF82NGFlOTUwMDAyZDQ0NTEyOTU5YWFmYTFhYjdkZDk4NC5zZXRDb250ZW50KGh0bWxfYTFmOTBmNjhmMmFjNDY0ZjhjNmE0OTczYjY5NDNhMzQpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIG1hcmtlcl8xOGFlNDg3MzhhZjI0ZDIwODcwZWRiMjgyYTY4ODA3My5iaW5kUG9wdXAocG9wdXBfNjRhZTk1MDAwMmQ0NDUxMjk1OWFhZmExYWI3ZGQ5ODQpOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAoKICAgICAgICAgICAgdmFyIG1hcmtlcl80YTc5ZDA4ZmQyNjc0OWE5ODgwNjk2ODRiNjIzYTAxZSA9IEwubWFya2VyKAogICAgICAgICAgICAgICAgWzUyLjUzNjQ4MDMsMS4wOTEyNTUyXSwKICAgICAgICAgICAgICAgIHsKICAgICAgICAgICAgICAgICAgICBpY29uOiBuZXcgTC5JY29uLkRlZmF1bHQoKQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgIC5hZGRUbyhtYXBfYWY1NTI1MTIwNDRjNDM1YjhkN2U5MDkyNmU3MGUwNGIpOwogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAgICAgCiAgICAgICAgICAgIHZhciBwb3B1cF8xOWUyYTJmNjJkZWY0ZjNlODY0YzU0YTIxZWEyODUwZCA9IEwucG9wdXAoe21heFdpZHRoOiAnMzAwJ30pOwoKICAgICAgICAgICAgCiAgICAgICAgICAgICAgICB2YXIgaHRtbF9jMDNkMzY1MjFlZWE0Mjg0YjYwOTA0NGQ2ODQyMDM4OSA9ICQoJyAgICAgICAgIDxkaXYgaWQ9Imh0bWxfYzAzZDM2NTIxZWVhNDI4NGI2MDkwNDRkNjg0MjAzODkiICAgICAgICAgICAgICAgICBzdHlsZT0id2lkdGg6IDEwMC4wJTsgaGVpZ2h0OiAxMDAuMCU7Ij4gICAgICAgICAgICAgICAgIEhBTExTIEp1bGlhbiBMYXdyZW5jZSwgKExpYmVyYWwgRGVtb2NyYXQpIFd5bW9uZGhhbTwvZGl2PiAgICAgICAgICAgICAgICAgJylbMF07CiAgICAgICAgICAgICAgICBwb3B1cF8xOWUyYTJmNjJkZWY0ZjNlODY0YzU0YTIxZWEyODUwZC5zZXRDb250ZW50KGh0bWxfYzAzZDM2NTIxZWVhNDI4NGI2MDkwNDRkNjg0MjAzODkpOwogICAgICAgICAgICAKCiAgICAgICAgICAgIG1hcmtlcl80YTc5ZDA4ZmQyNjc0OWE5ODgwNjk2ODRiNjIzYTAxZS5iaW5kUG9wdXAocG9wdXBfMTllMmEyZjYyZGVmNGYzZTg2NGM1NGEyMWVhMjg1MGQpOwoKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAoKICAgICAgICAgICAgdmFyIG1hcmtlcl8wOTMzYjBiNjZkZTE0NGUzYTg0YWU1MDZjZWMyZjRmNCA9IEwubWFya2VyKAogICAgICAgICAgICAgICAgWzUyLjU3MjM4NDYsMS4xMTg0M10sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfYzI2ZjZjNGRmOTU3NDhmOTg5ODllZjJlYTA4ZDQ1NWQgPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfMGIzNGI1MzU0YmM1NDUzZDkwOWEzYWQ2NWYxZGEwNzcgPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sXzBiMzRiNTM1NGJjNTQ1M2Q5MDlhM2FkNjVmMWRhMDc3IiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBNT09ORVkgSm9lLCAoQ29uc2VydmF0aXZlIFBhcnR5KSBXeW1vbmRoYW08L2Rpdj4gICAgICAgICAgICAgICAgICcpWzBdOwogICAgICAgICAgICAgICAgcG9wdXBfYzI2ZjZjNGRmOTU3NDhmOTg5ODllZjJlYTA4ZDQ1NWQuc2V0Q29udGVudChodG1sXzBiMzRiNTM1NGJjNTQ1M2Q5MDlhM2FkNjVmMWRhMDc3KTsKICAgICAgICAgICAgCgogICAgICAgICAgICBtYXJrZXJfMDkzM2IwYjY2ZGUxNDRlM2E4NGFlNTA2Y2VjMmY0ZjQuYmluZFBvcHVwKHBvcHVwX2MyNmY2YzRkZjk1NzQ4Zjk4OTg5ZWYyZWEwOGQ0NTVkKTsKCiAgICAgICAgICAgIAogICAgICAgIAogICAgICAgIAogICAgICAgICAgICAKCiAgICAgICAgICAgIHZhciBtYXJrZXJfNTE2MTk3N2U0OGY0NGVjMmI2ZGMzNjRhMmFjZDNmNzIgPSBMLm1hcmtlcigKICAgICAgICAgICAgICAgIFs1Mi41NzA4NDQ2LDEuMTI5NzI4Nl0sCiAgICAgICAgICAgICAgICB7CiAgICAgICAgICAgICAgICAgICAgaWNvbjogbmV3IEwuSWNvbi5EZWZhdWx0KCkKICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICApCiAgICAgICAgICAgICAgICAuYWRkVG8obWFwX2FmNTUyNTEyMDQ0YzQzNWI4ZDdlOTA5MjZlNzBlMDRiKTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAgICAgICAgIAogICAgICAgICAgICB2YXIgcG9wdXBfZWNhMGQ0OGEwYjZkNDRiZTg1ZmFkMDBjYTI5YzA4NjIgPSBMLnBvcHVwKHttYXhXaWR0aDogJzMwMCd9KTsKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGh0bWxfMmU5NTQ0ZmUwNDE5NGE0ZGIwOGMzY2RiOGZmNzEwNzUgPSAkKCcgICAgICAgICA8ZGl2IGlkPSJodG1sXzJlOTU0NGZlMDQxOTRhNGRiMDhjM2NkYjhmZjcxMDc1IiAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOiAxMDAuMCU7IGhlaWdodDogMTAwLjAlOyI+ICAgICAgICAgICAgICAgICBVTkRFUldPT0QgRG91ZywgKExhYm91ciBQYXJ0eSkgV3ltb25kaGFtPC9kaXY+ICAgICAgICAgICAgICAgICAnKVswXTsKICAgICAgICAgICAgICAgIHBvcHVwX2VjYTBkNDhhMGI2ZDQ0YmU4NWZhZDAwY2EyOWMwODYyLnNldENvbnRlbnQoaHRtbF8yZTk1NDRmZTA0MTk0YTRkYjA4YzNjZGI4ZmY3MTA3NSk7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgbWFya2VyXzUxNjE5NzdlNDhmNDRlYzJiNmRjMzY0YTJhY2QzZjcyLmJpbmRQb3B1cChwb3B1cF9lY2EwZDQ4YTBiNmQ0NGJlODVmYWQwMGNhMjljMDg2Mik7CgogICAgICAgICAgICAKICAgICAgICAKICAgICAgICAKICAgICAgICAKICAgICAgICA8L3NjcmlwdD4KICAgICAgICA=\" style=\"position:absolute;width:100%;height:100%;left:0;top:0;\">\n",
       "            </iframe>\n",
       "            </div></div>"
      ],
      "text/plain": [
       "<folium.folium.Map at 0x112adb410>"
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import folium\n",
    "\n",
    "def add_marker(row,fmap):\n",
    "    if row['latlong']!='':\n",
    "        lat=row['latlong'].split(',')[0]\n",
    "        long=row['latlong'].split(',')[1]\n",
    "        folium.Marker([lat, long], popup='{}, ({})\\n{}'.format(row['candidate'],row['desc'],row['ward'])).add_to(fmap)\n",
    "    \n",
    "#Create a map centered on the postcode location at a particular zoom level\n",
    "#Really crude centrepoint for map\n",
    "centrelatlong=candidates[candidates['latlong']!=''].iloc[0]['latlong'].split(',')\n",
    "\n",
    "\n",
    "localmap = folium.Map(location=centrelatlong, zoom_start=11)\n",
    "\n",
    "candidates.apply(lambda x: add_marker(x, localmap), axis=1)\n",
    "localmap"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "#save the map\n",
    "localmap.save(mapname)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Guess at Whether Candidates Live In-Ward or Out-of-Ward\n",
    "\n",
    "This could be a bit ropey - really need to check we are using the correct administrative geographies."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "deletable": true,
    "editable": true
   },
   "source": [
    "Use a service like [MapIt](https://mapit.mysociety.org/) or [postcodes.io](https://api.postcodes.io/) to find ward from postcode, then compare this to the name of the ward they are standing in."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ward</th>\n",
       "      <th>desc</th>\n",
       "      <th>candidate</th>\n",
       "      <th>address</th>\n",
       "      <th>latlong</th>\n",
       "      <th>postcode</th>\n",
       "      <th>pcward</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>BROWN Christopher John</td>\n",
       "      <td>Globe House, Norwich Road, Denton, Harleston, ...</td>\n",
       "      <td>52.448507,1.35477</td>\n",
       "      <td>IP20 0BD</td>\n",
       "      <td>Earsham</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>FOWLER Nicola Jeannette</td>\n",
       "      <td>21 Springfields, Poringland, Norwich, NR14 7RG</td>\n",
       "      <td>52.5693366,1.3469526</td>\n",
       "      <td>NR14 7RG</td>\n",
       "      <td>Poringland with the Framinghams</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>STONE Margaret Florence</td>\n",
       "      <td>25 Field Lane, Hempnall, Norwich, Norfolk, NR1...</td>\n",
       "      <td>52.4988471,1.298969</td>\n",
       "      <td>NR15 2QZ</td>\n",
       "      <td>Hempnall</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>EAST Tim</td>\n",
       "      <td>7 St Walstans Close, Costessey, Norwich, NR5 0TW</td>\n",
       "      <td>52.6460063,1.2041219</td>\n",
       "      <td>NR5 0TW</td>\n",
       "      <td>Old Costessey</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>GARRARD Jonathan Peter</td>\n",
       "      <td>68 Dereham Road, New Costessey, Norwich, NR5 0SY</td>\n",
       "      <td>52.642241,1.231012</td>\n",
       "      <td>NR5 0SY</td>\n",
       "      <td>New Costessey</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "        ward                desc                candidate  \\\n",
       "0  Clavering    Liberal Democrat   BROWN Christopher John   \n",
       "1  Clavering        Labour Party  FOWLER Nicola Jeannette   \n",
       "2  Clavering  Conservative Party  STONE Margaret Florence   \n",
       "3  Costessey    Liberal Democrat                 EAST Tim   \n",
       "4  Costessey        Labour Party   GARRARD Jonathan Peter   \n",
       "\n",
       "                                             address               latlong  \\\n",
       "0  Globe House, Norwich Road, Denton, Harleston, ...     52.448507,1.35477   \n",
       "1     21 Springfields, Poringland, Norwich, NR14 7RG  52.5693366,1.3469526   \n",
       "2  25 Field Lane, Hempnall, Norwich, Norfolk, NR1...   52.4988471,1.298969   \n",
       "3   7 St Walstans Close, Costessey, Norwich, NR5 0TW  52.6460063,1.2041219   \n",
       "4   68 Dereham Road, New Costessey, Norwich, NR5 0SY    52.642241,1.231012   \n",
       "\n",
       "   postcode                           pcward  \n",
       "0  IP20 0BD                          Earsham  \n",
       "1  NR14 7RG  Poringland with the Framinghams  \n",
       "2  NR15 2QZ                         Hempnall  \n",
       "3   NR5 0TW                    Old Costessey  \n",
       "4   NR5 0SY                    New Costessey  "
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import requests\n",
    "from ukpostcodeutils import validation\n",
    "\n",
    "def getpc(addr):\n",
    "    ''' Crude attempt to find postcode in address; conventionally last part of address in this dataset? '''\n",
    "    pc=addr.split(',')[-1].strip()\n",
    "    if validation.is_valid_postcode(pc.replace(' ','')): return pc\n",
    "    return ''\n",
    "\n",
    "def getpcward(pc):\n",
    "    ''' Lookup a ward from a postcode using postcodes.io '''\n",
    "    if pc!='':\n",
    "        try:\n",
    "            return requests.get('https://api.postcodes.io/postcodes/{}'.format(pc.replace(' ',''))).json()['result']['admin_ward']\n",
    "        except:\n",
    "            return ''\n",
    "    return ''\n",
    "\n",
    "#Extract the postcode - conventionally, it looks like postcode is last part of address so guess at that\n",
    "candidates['postcode']=candidates['address'].apply(getpc)\n",
    "\n",
    "#Get the list of unique postcodes for candidates and lookup the corresponding ward\n",
    "pcwards={pc: getpcward(pc) for pc in candidates['postcode'].unique()}\n",
    "\n",
    "candidates['pcward']=candidates['postcode'].map(pcwards)\n",
    "candidates.head()\n",
    "#If this doesn't catch anything - could also try to use latlong where no postcode available..."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ward</th>\n",
       "      <th>desc</th>\n",
       "      <th>candidate</th>\n",
       "      <th>address</th>\n",
       "      <th>latlong</th>\n",
       "      <th>postcode</th>\n",
       "      <th>pcward</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Empty DataFrame\n",
       "Columns: [ward, desc, candidate, address, latlong, postcode, pcward]\n",
       "Index: []"
      ]
     },
     "execution_count": 25,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#display in ward - so Ward they're standing in is same as ward of their address\n",
    "candidates[candidates['ward']==candidates['pcward']].head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ward</th>\n",
       "      <th>desc</th>\n",
       "      <th>candidate</th>\n",
       "      <th>address</th>\n",
       "      <th>latlong</th>\n",
       "      <th>postcode</th>\n",
       "      <th>pcward</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>BROWN Christopher John</td>\n",
       "      <td>Globe House, Norwich Road, Denton, Harleston, ...</td>\n",
       "      <td>52.448507,1.35477</td>\n",
       "      <td>IP20 0BD</td>\n",
       "      <td>Earsham</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>FOWLER Nicola Jeannette</td>\n",
       "      <td>21 Springfields, Poringland, Norwich, NR14 7RG</td>\n",
       "      <td>52.5693366,1.3469526</td>\n",
       "      <td>NR14 7RG</td>\n",
       "      <td>Poringland with the Framinghams</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>STONE Margaret Florence</td>\n",
       "      <td>25 Field Lane, Hempnall, Norwich, Norfolk, NR1...</td>\n",
       "      <td>52.4988471,1.298969</td>\n",
       "      <td>NR15 2QZ</td>\n",
       "      <td>Hempnall</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>EAST Tim</td>\n",
       "      <td>7 St Walstans Close, Costessey, Norwich, NR5 0TW</td>\n",
       "      <td>52.6460063,1.2041219</td>\n",
       "      <td>NR5 0TW</td>\n",
       "      <td>Old Costessey</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>GARRARD Jonathan Peter</td>\n",
       "      <td>68 Dereham Road, New Costessey, Norwich, NR5 0SY</td>\n",
       "      <td>52.642241,1.231012</td>\n",
       "      <td>NR5 0SY</td>\n",
       "      <td>New Costessey</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Green Party</td>\n",
       "      <td>ROWETT Catherine Joanna</td>\n",
       "      <td>10 Caroline Court, Norwich, NR4 7EJ</td>\n",
       "      <td>52.6214876,1.2628925</td>\n",
       "      <td>NR4 7EJ</td>\n",
       "      <td>Eaton</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>Costessey</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>WILTSHIRE Andrew Roy</td>\n",
       "      <td>13 Cardinal Close, Easton, Norwich, NR9 5EW</td>\n",
       "      <td>52.654118,1.1620887</td>\n",
       "      <td>NR9 5EW</td>\n",
       "      <td>Easton</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>Diss and Roydon</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>DAVISON Chris</td>\n",
       "      <td>1 Willbye Avenue, Diss, Norfolk, IP22 4NN</td>\n",
       "      <td>52.3788722,1.1162182</td>\n",
       "      <td>IP22 4NN</td>\n",
       "      <td>Diss</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>Diss and Roydon</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>KIDDIE Keith Walter</td>\n",
       "      <td>17 Walcot Road, Diss, Norfolk, IP22 4DB</td>\n",
       "      <td>52.3812672,1.1136278</td>\n",
       "      <td>IP22 4DB</td>\n",
       "      <td>Diss</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>Diss and Roydon</td>\n",
       "      <td>Green Party</td>\n",
       "      <td>MILTON David</td>\n",
       "      <td>18 Friars Quay, Norwich, Norfolk, NR3 1ES</td>\n",
       "      <td>52.6326424,1.2961341</td>\n",
       "      <td>NR3 1ES</td>\n",
       "      <td>Mancroft</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10</th>\n",
       "      <td>Diss and Roydon</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>SCOGGINS Tracy Barbara</td>\n",
       "      <td>22 Spencer Crescent, Diss, Norfolk, IP22 4UF</td>\n",
       "      <td></td>\n",
       "      <td>IP22 4UF</td>\n",
       "      <td>Diss</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>11</th>\n",
       "      <td>East Depwade</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>EDDY James William</td>\n",
       "      <td>11 Henry Ward Road, Harleston, Norfolk, IP20 9EZ</td>\n",
       "      <td></td>\n",
       "      <td>IP20 9EZ</td>\n",
       "      <td>Harleston</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>12</th>\n",
       "      <td>East Depwade</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>KUZMIC Susan Evelyn</td>\n",
       "      <td>29 Gawdy Close, Harleston, IP20 9ET</td>\n",
       "      <td>52.4077753,1.300708</td>\n",
       "      <td>IP20 9ET</td>\n",
       "      <td>Harleston</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>13</th>\n",
       "      <td>East Depwade</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>WILBY Martin James</td>\n",
       "      <td>New Lodge Farm, Common Road, Dickleburgh, Diss...</td>\n",
       "      <td></td>\n",
       "      <td>IP21 4PH</td>\n",
       "      <td>Dickleburgh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>14</th>\n",
       "      <td>Forehoe</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>FOULGER Colin Wayne</td>\n",
       "      <td>Pear Tree House, The Turnpike, Bunwell, Norwic...</td>\n",
       "      <td></td>\n",
       "      <td>NR16 1SP</td>\n",
       "      <td>Bunwell</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>15</th>\n",
       "      <td>Forehoe</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>MCCLENNING Robert Arthur</td>\n",
       "      <td>Brunel, Cheneys Lane, Tacolneston, Norwich, NR...</td>\n",
       "      <td></td>\n",
       "      <td>NR16 1DB</td>\n",
       "      <td>Forncett</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>16</th>\n",
       "      <td>Forehoe</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>SEWELL Steven Leigh</td>\n",
       "      <td>Medway, The Rosery, Mulbarton, Norwich, NR14 8AL</td>\n",
       "      <td></td>\n",
       "      <td>NR14 8AL</td>\n",
       "      <td>Mulbarton</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>17</th>\n",
       "      <td>Henstead</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>FOWLER Tom</td>\n",
       "      <td>21 Springfields, Poringland, Norwich, NR14 7RG</td>\n",
       "      <td>52.5693366,1.3469526</td>\n",
       "      <td>NR14 7RG</td>\n",
       "      <td>Poringland with the Framinghams</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>18</th>\n",
       "      <td>Henstead</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>HAMMOND Matthew</td>\n",
       "      <td>6 Church Farm Barns, The Street, Bramerton, NR...</td>\n",
       "      <td></td>\n",
       "      <td>NR14 7DW</td>\n",
       "      <td>Rockland</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>19</th>\n",
       "      <td>Henstead</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>THOMSON Vic</td>\n",
       "      <td>Yelverton Hall, Yelverton, Norwich, Norfolk, N...</td>\n",
       "      <td>52.5733553,1.3568878</td>\n",
       "      <td>NR14 7PD</td>\n",
       "      <td>Rockland</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>20</th>\n",
       "      <td>Hingham</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>BLATHWAYT Paul Wynter</td>\n",
       "      <td>Rivendell, 21 Marlingford Lane, Easton, Norwic...</td>\n",
       "      <td></td>\n",
       "      <td>NR9 5AD</td>\n",
       "      <td>Easton</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21</th>\n",
       "      <td>Hingham</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>DEWSBURY Margaret</td>\n",
       "      <td>6 Park Avenue, Barford, Norwich, Norfolk, NR9 4BA</td>\n",
       "      <td>52.6250533,1.1238474</td>\n",
       "      <td>NR9 4BA</td>\n",
       "      <td>Easton</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>22</th>\n",
       "      <td>Hingham</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>LEMAN James Edward George</td>\n",
       "      <td>48 Silfield Road, Wymondham, NR18 9AY</td>\n",
       "      <td>52.5597768,1.1202557</td>\n",
       "      <td>NR18 9AY</td>\n",
       "      <td>Cromwells</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23</th>\n",
       "      <td>Humbleyard</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>BILLS David</td>\n",
       "      <td>3 Beech Court, Norwich Road, Hethersett, Norwi...</td>\n",
       "      <td>52.597855,1.1817466</td>\n",
       "      <td>NR9 3FE</td>\n",
       "      <td>Hethersett</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>24</th>\n",
       "      <td>Humbleyard</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>GULLIVER Bethan Sin</td>\n",
       "      <td>Laurel House, Norwich Road, Tacolneston, Norwi...</td>\n",
       "      <td>52.5074631,1.1567953</td>\n",
       "      <td>NR16 1BY</td>\n",
       "      <td>Forncett</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>25</th>\n",
       "      <td>Humbleyard</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>SUTTON Jacky</td>\n",
       "      <td>12 Childs Road, Hethersett, NR9 3HN</td>\n",
       "      <td>52.6002644,1.1661295</td>\n",
       "      <td>NR9 3HN</td>\n",
       "      <td>Hethersett</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>26</th>\n",
       "      <td>Loddon</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>BINGHAM David Kenneth</td>\n",
       "      <td>19 Gale Close, Hales, Norwich, NR14 6SN</td>\n",
       "      <td>52.5204002,1.5095713</td>\n",
       "      <td>NR14 6SN</td>\n",
       "      <td>Gillingham</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>27</th>\n",
       "      <td>Loddon</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>BISSONNET David George</td>\n",
       "      <td>Duck Cottage, 3 Ferry Road, Carleton St Peter,...</td>\n",
       "      <td>52.5764436,1.463634</td>\n",
       "      <td>NR14 7AY</td>\n",
       "      <td>Chedgrave and Thurton</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>28</th>\n",
       "      <td>Loddon</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>STONE Barry Michael</td>\n",
       "      <td>25 Field Lane, Hempnall, Norwich, Norfolk, NR1...</td>\n",
       "      <td>52.4988471,1.298969</td>\n",
       "      <td>NR15 2QZ</td>\n",
       "      <td>Hempnall</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>29</th>\n",
       "      <td>Long Stratton</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>KATZ Elana</td>\n",
       "      <td>The Farmhouse, Wolsey Farm, Durbidges Hill, Di...</td>\n",
       "      <td></td>\n",
       "      <td>IP22 5SY</td>\n",
       "      <td>Bressingham and Burston</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>30</th>\n",
       "      <td>Long Stratton</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>PERCIVAL Roger Neil</td>\n",
       "      <td>The Barn, Rattees Corner, Hapton Road, Fundenh...</td>\n",
       "      <td></td>\n",
       "      <td>NR16 1EQ</td>\n",
       "      <td>Forncett</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>31</th>\n",
       "      <td>Long Stratton</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>THOMAS Alison Mary</td>\n",
       "      <td>Briardale, Ipswich Road, Long Stratton, Norwic...</td>\n",
       "      <td></td>\n",
       "      <td>NR15 2TF</td>\n",
       "      <td>Stratton</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>32</th>\n",
       "      <td>West Depwade</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>REEKIE Pam</td>\n",
       "      <td>The White House, Ipswich Road, Dickleburgh, IP...</td>\n",
       "      <td></td>\n",
       "      <td>IP21 4NJ</td>\n",
       "      <td>Dickleburgh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>33</th>\n",
       "      <td>West Depwade</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>SPRATT Beverley Herbert Allison</td>\n",
       "      <td>Lakes Farm, Hall Road, Tacolneston, Norwich, N...</td>\n",
       "      <td></td>\n",
       "      <td>NR16 1DN</td>\n",
       "      <td>Forncett</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>34</th>\n",
       "      <td>West Depwade</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>SPRATT Ian Victor</td>\n",
       "      <td>29 Knyvett Green, Ashwellthorpe, Norwich, Norf...</td>\n",
       "      <td>52.5334951,1.159976</td>\n",
       "      <td>NR16 1HA</td>\n",
       "      <td>Forncett</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>35</th>\n",
       "      <td>Wymondham</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "      <td>HALLS Julian Lawrence</td>\n",
       "      <td>2 Chapel Loke, Spooner Row, Wymondham, NR18 9LS</td>\n",
       "      <td>52.5364803,1.0912552</td>\n",
       "      <td>NR18 9LS</td>\n",
       "      <td>Cromwells</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>36</th>\n",
       "      <td>Wymondham</td>\n",
       "      <td>Conservative Party</td>\n",
       "      <td>MOONEY Joe</td>\n",
       "      <td>2 Orchard Way, Wymondham, Norfolk, NR18 0NX</td>\n",
       "      <td>52.5723846,1.11843</td>\n",
       "      <td>NR18 0NX</td>\n",
       "      <td>Town</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>37</th>\n",
       "      <td>Wymondham</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>UNDERWOOD Doug</td>\n",
       "      <td>14 Herb Robert Glade, Wymondham, Norfolk, NR18...</td>\n",
       "      <td>52.5708446,1.1297286</td>\n",
       "      <td>NR18 0XS</td>\n",
       "      <td>Town</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "               ward                desc                        candidate  \\\n",
       "0         Clavering    Liberal Democrat           BROWN Christopher John   \n",
       "1         Clavering        Labour Party          FOWLER Nicola Jeannette   \n",
       "2         Clavering  Conservative Party          STONE Margaret Florence   \n",
       "3         Costessey    Liberal Democrat                         EAST Tim   \n",
       "4         Costessey        Labour Party           GARRARD Jonathan Peter   \n",
       "5         Costessey         Green Party          ROWETT Catherine Joanna   \n",
       "6         Costessey  Conservative Party             WILTSHIRE Andrew Roy   \n",
       "7   Diss and Roydon        Labour Party                    DAVISON Chris   \n",
       "8   Diss and Roydon  Conservative Party              KIDDIE Keith Walter   \n",
       "9   Diss and Roydon         Green Party                     MILTON David   \n",
       "10  Diss and Roydon    Liberal Democrat           SCOGGINS Tracy Barbara   \n",
       "11     East Depwade        Labour Party               EDDY James William   \n",
       "12     East Depwade    Liberal Democrat              KUZMIC Susan Evelyn   \n",
       "13     East Depwade  Conservative Party               WILBY Martin James   \n",
       "14          Forehoe  Conservative Party              FOULGER Colin Wayne   \n",
       "15          Forehoe    Liberal Democrat         MCCLENNING Robert Arthur   \n",
       "16          Forehoe        Labour Party              SEWELL Steven Leigh   \n",
       "17         Henstead        Labour Party                       FOWLER Tom   \n",
       "18         Henstead    Liberal Democrat                  HAMMOND Matthew   \n",
       "19         Henstead  Conservative Party                      THOMSON Vic   \n",
       "20          Hingham    Liberal Democrat            BLATHWAYT Paul Wynter   \n",
       "21          Hingham  Conservative Party                DEWSBURY Margaret   \n",
       "22          Hingham        Labour Party        LEMAN James Edward George   \n",
       "23       Humbleyard  Conservative Party                      BILLS David   \n",
       "24       Humbleyard        Labour Party              GULLIVER Bethan Sin   \n",
       "25       Humbleyard    Liberal Democrat                     SUTTON Jacky   \n",
       "26           Loddon    Liberal Democrat            BINGHAM David Kenneth   \n",
       "27           Loddon        Labour Party           BISSONNET David George   \n",
       "28           Loddon  Conservative Party              STONE Barry Michael   \n",
       "29    Long Stratton        Labour Party                       KATZ Elana   \n",
       "30    Long Stratton    Liberal Democrat              PERCIVAL Roger Neil   \n",
       "31    Long Stratton  Conservative Party               THOMAS Alison Mary   \n",
       "32     West Depwade        Labour Party                       REEKIE Pam   \n",
       "33     West Depwade  Conservative Party  SPRATT Beverley Herbert Allison   \n",
       "34     West Depwade    Liberal Democrat                SPRATT Ian Victor   \n",
       "35        Wymondham    Liberal Democrat            HALLS Julian Lawrence   \n",
       "36        Wymondham  Conservative Party                       MOONEY Joe   \n",
       "37        Wymondham        Labour Party                   UNDERWOOD Doug   \n",
       "\n",
       "                                              address               latlong  \\\n",
       "0   Globe House, Norwich Road, Denton, Harleston, ...     52.448507,1.35477   \n",
       "1      21 Springfields, Poringland, Norwich, NR14 7RG  52.5693366,1.3469526   \n",
       "2   25 Field Lane, Hempnall, Norwich, Norfolk, NR1...   52.4988471,1.298969   \n",
       "3    7 St Walstans Close, Costessey, Norwich, NR5 0TW  52.6460063,1.2041219   \n",
       "4    68 Dereham Road, New Costessey, Norwich, NR5 0SY    52.642241,1.231012   \n",
       "5                 10 Caroline Court, Norwich, NR4 7EJ  52.6214876,1.2628925   \n",
       "6         13 Cardinal Close, Easton, Norwich, NR9 5EW   52.654118,1.1620887   \n",
       "7           1 Willbye Avenue, Diss, Norfolk, IP22 4NN  52.3788722,1.1162182   \n",
       "8             17 Walcot Road, Diss, Norfolk, IP22 4DB  52.3812672,1.1136278   \n",
       "9           18 Friars Quay, Norwich, Norfolk, NR3 1ES  52.6326424,1.2961341   \n",
       "10       22 Spencer Crescent, Diss, Norfolk, IP22 4UF                         \n",
       "11   11 Henry Ward Road, Harleston, Norfolk, IP20 9EZ                         \n",
       "12                29 Gawdy Close, Harleston, IP20 9ET   52.4077753,1.300708   \n",
       "13  New Lodge Farm, Common Road, Dickleburgh, Diss...                         \n",
       "14  Pear Tree House, The Turnpike, Bunwell, Norwic...                         \n",
       "15  Brunel, Cheneys Lane, Tacolneston, Norwich, NR...                         \n",
       "16   Medway, The Rosery, Mulbarton, Norwich, NR14 8AL                         \n",
       "17     21 Springfields, Poringland, Norwich, NR14 7RG  52.5693366,1.3469526   \n",
       "18  6 Church Farm Barns, The Street, Bramerton, NR...                         \n",
       "19  Yelverton Hall, Yelverton, Norwich, Norfolk, N...  52.5733553,1.3568878   \n",
       "20  Rivendell, 21 Marlingford Lane, Easton, Norwic...                         \n",
       "21  6 Park Avenue, Barford, Norwich, Norfolk, NR9 4BA  52.6250533,1.1238474   \n",
       "22              48 Silfield Road, Wymondham, NR18 9AY  52.5597768,1.1202557   \n",
       "23  3 Beech Court, Norwich Road, Hethersett, Norwi...   52.597855,1.1817466   \n",
       "24  Laurel House, Norwich Road, Tacolneston, Norwi...  52.5074631,1.1567953   \n",
       "25                12 Childs Road, Hethersett, NR9 3HN  52.6002644,1.1661295   \n",
       "26            19 Gale Close, Hales, Norwich, NR14 6SN  52.5204002,1.5095713   \n",
       "27  Duck Cottage, 3 Ferry Road, Carleton St Peter,...   52.5764436,1.463634   \n",
       "28  25 Field Lane, Hempnall, Norwich, Norfolk, NR1...   52.4988471,1.298969   \n",
       "29  The Farmhouse, Wolsey Farm, Durbidges Hill, Di...                         \n",
       "30  The Barn, Rattees Corner, Hapton Road, Fundenh...                         \n",
       "31  Briardale, Ipswich Road, Long Stratton, Norwic...                         \n",
       "32  The White House, Ipswich Road, Dickleburgh, IP...                         \n",
       "33  Lakes Farm, Hall Road, Tacolneston, Norwich, N...                         \n",
       "34  29 Knyvett Green, Ashwellthorpe, Norwich, Norf...   52.5334951,1.159976   \n",
       "35    2 Chapel Loke, Spooner Row, Wymondham, NR18 9LS  52.5364803,1.0912552   \n",
       "36        2 Orchard Way, Wymondham, Norfolk, NR18 0NX    52.5723846,1.11843   \n",
       "37  14 Herb Robert Glade, Wymondham, Norfolk, NR18...  52.5708446,1.1297286   \n",
       "\n",
       "    postcode                           pcward  \n",
       "0   IP20 0BD                          Earsham  \n",
       "1   NR14 7RG  Poringland with the Framinghams  \n",
       "2   NR15 2QZ                         Hempnall  \n",
       "3    NR5 0TW                    Old Costessey  \n",
       "4    NR5 0SY                    New Costessey  \n",
       "5    NR4 7EJ                            Eaton  \n",
       "6    NR9 5EW                           Easton  \n",
       "7   IP22 4NN                             Diss  \n",
       "8   IP22 4DB                             Diss  \n",
       "9    NR3 1ES                         Mancroft  \n",
       "10  IP22 4UF                             Diss  \n",
       "11  IP20 9EZ                        Harleston  \n",
       "12  IP20 9ET                        Harleston  \n",
       "13  IP21 4PH                      Dickleburgh  \n",
       "14  NR16 1SP                          Bunwell  \n",
       "15  NR16 1DB                         Forncett  \n",
       "16  NR14 8AL                        Mulbarton  \n",
       "17  NR14 7RG  Poringland with the Framinghams  \n",
       "18  NR14 7DW                         Rockland  \n",
       "19  NR14 7PD                         Rockland  \n",
       "20   NR9 5AD                           Easton  \n",
       "21   NR9 4BA                           Easton  \n",
       "22  NR18 9AY                        Cromwells  \n",
       "23   NR9 3FE                       Hethersett  \n",
       "24  NR16 1BY                         Forncett  \n",
       "25   NR9 3HN                       Hethersett  \n",
       "26  NR14 6SN                       Gillingham  \n",
       "27  NR14 7AY            Chedgrave and Thurton  \n",
       "28  NR15 2QZ                         Hempnall  \n",
       "29  IP22 5SY          Bressingham and Burston  \n",
       "30  NR16 1EQ                         Forncett  \n",
       "31  NR15 2TF                         Stratton  \n",
       "32  IP21 4NJ                      Dickleburgh  \n",
       "33  NR16 1DN                         Forncett  \n",
       "34  NR16 1HA                         Forncett  \n",
       "35  NR18 9LS                        Cromwells  \n",
       "36  NR18 0NX                             Town  \n",
       "37  NR18 0XS                             Town  "
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#display out ward - so Ward they're standing in is not the same as ward of their address\n",
    "candidates[candidates['ward']!=candidates['pcward']]#.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "deletable": true,
    "editable": true
   },
   "source": [
    "## Chart cross-support\n",
    "\n",
    "From the table of supporters, we can try to identify candidates who support other candidates."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>candinit</th>\n",
       "      <th>role</th>\n",
       "      <th>candidate</th>\n",
       "      <th>support</th>\n",
       "      <th>typ</th>\n",
       "      <th>ward</th>\n",
       "      <th>desc</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Christopher J. Brown</td>\n",
       "      <td>proposal</td>\n",
       "      <td>BROWN Christopher John</td>\n",
       "      <td>Murray Gray</td>\n",
       "      <td>proposer</td>\n",
       "      <td>Clavering</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Christopher J. Brown</td>\n",
       "      <td>proposal</td>\n",
       "      <td>BROWN Christopher John</td>\n",
       "      <td>Richard A P Carden</td>\n",
       "      <td>assentor</td>\n",
       "      <td>Clavering</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Christopher J. Brown</td>\n",
       "      <td>proposal</td>\n",
       "      <td>BROWN Christopher John</td>\n",
       "      <td>Noelle R M Barber</td>\n",
       "      <td>assentor</td>\n",
       "      <td>Clavering</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Christopher J. Brown</td>\n",
       "      <td>proposal</td>\n",
       "      <td>BROWN Christopher John</td>\n",
       "      <td>Reginald A Kirkpatrick</td>\n",
       "      <td>assentor</td>\n",
       "      <td>Clavering</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Christopher J. Brown</td>\n",
       "      <td>proposal</td>\n",
       "      <td>BROWN Christopher John</td>\n",
       "      <td>Paul E J Chaston</td>\n",
       "      <td>assentor</td>\n",
       "      <td>Clavering</td>\n",
       "      <td>Liberal Democrat</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "               candinit      role               candidate  \\\n",
       "0  Christopher J. Brown  proposal  BROWN Christopher John   \n",
       "1  Christopher J. Brown  proposal  BROWN Christopher John   \n",
       "2  Christopher J. Brown  proposal  BROWN Christopher John   \n",
       "3  Christopher J. Brown  proposal  BROWN Christopher John   \n",
       "4  Christopher J. Brown  proposal  BROWN Christopher John   \n",
       "\n",
       "                  support       typ       ward              desc  \n",
       "0             Murray Gray  proposer  Clavering  Liberal Democrat  \n",
       "1      Richard A P Carden  assentor  Clavering  Liberal Democrat  \n",
       "2       Noelle R M Barber  assentor  Clavering  Liberal Democrat  \n",
       "3  Reginald A Kirkpatrick  assentor  Clavering  Liberal Democrat  \n",
       "4        Paul E J Chaston  assentor  Clavering  Liberal Democrat  "
      ]
     },
     "execution_count": 27,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Preview the supporters table\n",
    "supporters = pd.read_sql_query(\"SELECT * FROM support\", conn)\n",
    "#Clean the data a bit\n",
    "supporters['desc']=supporters['desc'].str.replace('The ','').str.replace(' Candidate','')\n",
    "supporters.head(5)\n",
    "\n",
    "supporters.head(5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {
    "collapsed": false
   },
   "outputs": [],
   "source": [
    "#Save supportes data file\n",
    "supporters.to_csv(supportersfilename,index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([u'Liberal Democrat', u'Labour Party', u'Conservative Party',\n",
       "       u'Green Party'], dtype=object)"
      ]
     },
     "execution_count": 29,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Find the unique parties\n",
    "supporters['desc'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {
    "collapsed": true,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "colourmap={'Liberal Democrat':'yellow', 'Independent':'black', 'Labour Party':\"red\",\n",
    "       'Conservative Party':'blue', 'Green Party':'green', 'UKIP':'purple',\n",
    "       'Labour and Co- operative Party':'red'}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {
    "collapsed": true,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "#Create a graph\n",
    "import networkx as nx"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "#G=nx.from_pandas_dataframe(supporters, 'support', 'candinit')\n",
    "def build_graph(row,DG):\n",
    "    DG.add_node(row['support'],color=colourmap[row['desc']])\n",
    "    DG.add_node(row['candinit'],color=colourmap[row['desc']])\n",
    "    DG.add_edge(row['support'],row['candinit'],color=colourmap[row['desc']])\n",
    "    return\n",
    "\n",
    "DG=nx.DiGraph()\n",
    "supporters.apply(lambda x: build_graph(x,DG), axis=1);"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "nodes = DG.nodes()\n",
    "edges = DG.edges()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "#filter on people who are supported and who support\n",
    "supports_deg = DG.out_degree(nodes)\n",
    "supported_deg = DG.in_degree(nodes)\n",
    "supports = [n for n in supports_deg if supports_deg[n]]\n",
    "supported = [n for n in supported_deg if supported_deg[n]]\n",
    "\n",
    "GG=nx.DiGraph()\n",
    "#Merge the egographs of people of people who support and are supported\n",
    "for s2 in list(set(supports).intersection(set(supported))):\n",
    "    GG=nx.compose(GG,nx.ego_graph(DG,s2,5))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true,
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<!doctype html><html><head>  <title>Network | Basic usage</title></head><body><script type=\"text/javascript\">function setUpFrame() {     var frame = window.frames[\"style_file0\"];    frame.runVis([{\"node_shape\": \"dot\", \"degree\": 3.0, \"title\": \"Pam Reekie\", \"color\": \"red\", \"y\": 0.0, \"x\": 0.0, \"border_width\": 0, \"id\": \"Pam Reekie\"}, {\"node_shape\": \"dot\", \"degree\": 3.0, \"title\": \"Elana Katz\", \"color\": \"red\", \"y\": 0.99413895328175628, \"x\": 1.0, \"border_width\": 0, \"id\": \"Elana Katz\"}], [{\"color\": \"red\", \"source\": 1, \"target\": 0, \"title\": \"test\"}]);}</script><iframe name=\"style_file0\" src=\"style_file0.html\" height=\"1200px\" width=\"100%;\"></iframe></body></html>"
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "execution_count": 35,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#http://bl.ocks.org/brinrosenthal/raw/cfb0e12f113d55551a45d530527baedf/\n",
    "import visJS2jupyter.visJS_module\n",
    "nodes = GG.nodes()\n",
    "edges = GG.edges()\n",
    "\n",
    "pos = nx.spring_layout(GG)\n",
    "nodes_dict = [{\"id\":n,\"color\":GG.node[n]['color'],\n",
    "              \"x\":pos[n][0],\n",
    "              \"y\":pos[n][1]} for n in nodes]\n",
    "node_map = dict(zip(nodes,range(len(nodes))))  # map to indices for source/target in edges\n",
    "\n",
    "edges_dict = [{\"source\":node_map[edges[i][0]], \"target\":node_map[edges[i][1]], \"color\":GG[edges[i][0]][edges[i][1]]['color'],\n",
    "              \"title\":'test'} for i in range(len(edges))]\n",
    "\n",
    "visJS2jupyter.visJS_module.visjs_network(nodes_dict,edges_dict)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "metadata": {
    "collapsed": false
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(u'Elana Katz', u'Pam Reekie')\n"
     ]
    }
   ],
   "source": [
    "#Support between connected candidates where a candidate supports another candidate\n",
    "for e in edges:\n",
    "    print(e)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "deletable": true,
    "editable": true
   },
   "source": [
    "## Look for people with same name offering support to multiple candidates\n",
    "\n",
    "Does it look like the same person is supporting more than one candidate?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>candinit</th>\n",
       "      <th>role</th>\n",
       "      <th>candidate</th>\n",
       "      <th>support</th>\n",
       "      <th>typ</th>\n",
       "      <th>ward</th>\n",
       "      <th>desc</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Empty DataFrame\n",
       "Columns: [candinit, role, candidate, support, typ, ward, desc]\n",
       "Index: []"
      ]
     },
     "execution_count": 36,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "supporters[supporters['support'].isin(supporters[supporters.duplicated(subset='support')]['support'].unique())]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>candinit</th>\n",
       "      <th>role</th>\n",
       "      <th>candidate</th>\n",
       "      <th>support</th>\n",
       "      <th>typ</th>\n",
       "      <th>ward</th>\n",
       "      <th>desc</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Empty DataFrame\n",
       "Columns: [candinit, role, candidate, support, typ, ward, desc]\n",
       "Index: []"
      ]
     },
     "execution_count": 37,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Another way of doing that\n",
    "pd.read_sql_query(\"SELECT * FROM support WHERE support=(SELECT support FROM support GROUP BY support HAVING COUNT(*)>1)\", conn)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "deletable": true,
    "editable": true
   },
   "source": [
    "## Look for candidates sharing the same address\n",
    "\n",
    "Does it look like multiple candidates share the same address?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ward</th>\n",
       "      <th>desc</th>\n",
       "      <th>candidate</th>\n",
       "      <th>address</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Clavering</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>FOWLER Nicola Jeannette</td>\n",
       "      <td>21 Springfields, Poringland, Norwich, NR14 7RG</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Henstead</td>\n",
       "      <td>Labour Party</td>\n",
       "      <td>FOWLER Tom</td>\n",
       "      <td>21 Springfields, Poringland, Norwich, NR14 7RG</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "        ward          desc                candidate  \\\n",
       "0  Clavering  Labour Party  FOWLER Nicola Jeannette   \n",
       "1   Henstead  Labour Party               FOWLER Tom   \n",
       "\n",
       "                                          address  \n",
       "0  21 Springfields, Poringland, Norwich, NR14 7RG  \n",
       "1  21 Springfields, Poringland, Norwich, NR14 7RG  "
      ]
     },
     "execution_count": 38,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "## Multiple candidates from one address\n",
    "\n",
    "pd.read_sql_query(\"SELECT * FROM candidates WHERE address=(SELECT address FROM candidates GROUP BY address HAVING COUNT(*)>1)\", conn)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "deletable": true,
    "editable": true
   },
   "source": [
    "## Look for the same party standing multiple candidates in the same ward\n",
    "\n",
    "Does it look like the same party is supporting more than one candidate in a particular ward?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ward</th>\n",
       "      <th>desc</th>\n",
       "      <th>count(*)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "Empty DataFrame\n",
       "Columns: [ward, desc, count(*)]\n",
       "Index: []"
      ]
     },
     "execution_count": 39,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "## Multiple Candidates for a Party in Same Ward\n",
    "\n",
    "pd.read_sql_query(\"SELECT ward,desc, count(*) FROM support WHERE typ='proposer' GROUP BY ward,desc HAVING COUNT(*)>1\", conn)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "deletable": true,
    "editable": true
   },
   "source": [
    "## Companies House / OpenCorporates Lookup\n",
    "\n",
    "Check to see whether the names of candidates are also possible company directors.\n",
    "\n",
    "Could also do a check to see if they are charity trustees, bankrupt, disqualified director, registered licensee on any IW Council registers etc etc.\n",
    "\n",
    "__NOTE THAT THE FOLLOWING DOES NOT GUARANTEE OR NECESSARILY IMPLY THAT THE PERSON NAMED AS STANDING IS THE SAME PERSON AS A SIMILARLY NAMED COMPANY OFFICER.__"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {
    "collapsed": true,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "import urllib2, base64, json\n",
    "from urllib import urlencode\n",
    "from time import sleep\n",
    "\n",
    "def url_nice_req(url,t=300):\n",
    "    try:\n",
    "        return urllib2.urlopen(url)\n",
    "    except urllib2.HTTPError, e:\n",
    "        if e.code == 429:\n",
    "            print(\"Overloaded API, resting for a bit...\")\n",
    "            sleep(t)\n",
    "            return url_req(url)\n",
    "        \n",
    "#Inspired by http://stackoverflow.com/a/2955687/454773\n",
    "def ch_request(CH_API_TOKEN,url,args=None):\n",
    "    if args is not None:\n",
    "        url='{}?{}'.format(url,urlencode(args))\n",
    "    request = urllib2.Request(url)\n",
    "    # You need the replace to handle encodestring adding a trailing newline \n",
    "    # (https://docs.python.org/2/library/base64.html#base64.encodestring)\n",
    "    base64string = base64.encodestring('%s:' % (CH_API_TOKEN)).replace('\\n', '')\n",
    "    request.add_header(\"Authorization\", \"Basic %s\" % base64string)   \n",
    "    result = url_nice_req(request)\n",
    "\n",
    "    #This is too hacky - need to see why it fails if it does\n",
    "    if result is None:\n",
    "        print('Oops: {}, {}'.format(url,result))\n",
    "        return None\n",
    "        \n",
    "    j=json.loads(result.read())        \n",
    "        \n",
    "    return j"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {
    "collapsed": true,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "def ch_getAppointments(slug,location=None,typ='all',role='all',n=500,start_index=''):\n",
    "    if len(slug.split('/'))==1:\n",
    "        slug='/officers/{}/appointments'.format(slug)\n",
    "    url= 'https://api.companieshouse.gov.uk{}'.format(slug)\n",
    "    properties={'items_per_page':n,'start_index':start_index}\n",
    "    a=ch_request(CH_API_TOKEN,url,properties)\n",
    "\n",
    "    if a is None: return None\n",
    "    \n",
    "    if location is not None:\n",
    "        a['items']=[i for i in a['items'] if location.lower() in i['address']['locality'].lower()]\n",
    "    if typ=='current':\n",
    "        a['items']=[i for i in a['items'] if 'resigned_on' not in i]\n",
    "        a['items']=[i for i in a['items'] if 'company_status' in i['appointed_to'] and i['appointed_to']['company_status'] == 'active']\n",
    "        #should possibly check here that len(co['items'])==co['active_count'] ?\n",
    "    elif typ=='previous':\n",
    "        a['items']=[i for i in a['items'] if 'resigned_on' in i]\n",
    "    elif typ=='dissolved':\n",
    "        a['items']=[i for i in a['items'] if 'company_status' in i['appointed_to'] and i['appointed_to']['company_status'] == 'dissolved']\n",
    "\n",
    "    if role!='all':\n",
    "        a['items']=[i for i in a['items'] if role==i['officer_role']]\n",
    "    return a"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {
    "collapsed": true,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "def ch_searchOfficers(name,n=50,start_index='',company='',companies=False,exact=None):\n",
    "    url= 'https://api.companieshouse.gov.uk/search/officers'\n",
    "    properties={'q':name,'items_per_page':n,'start_index':start_index} \n",
    "    o=ch_request(CH_API_TOKEN,url,properties)\n",
    "    \n",
    "    if o is None: return o\n",
    "    \n",
    "    if exact=='forename':\n",
    "        #This isn't right eg double barrelled surnames\n",
    "        s=name.lower().split(' ')\n",
    "        o['items'] = [i for i in o['items'] if i['title'].lower().split(' ')[0]==s[0] and i['title'].lower().split(' ')[-1]==s[-1]]\n",
    "    elif exact=='fullname':\n",
    "        o['items'] = [i for i in o['items'] if i['title'].lower()==name.lower()]\n",
    "    if company != '':\n",
    "        for p in o['items']:\n",
    "            p['items'] = [i for i in ch_getAppointments(p['links']['self'])['items'] if company.lower() in i['appointed_to']['company_name'].lower()]\n",
    "        o['items'] = [i for i in o['items'] if len(i['items'])]\n",
    "    if companies:\n",
    "        for p in o['items']:\n",
    "            p['items'] = [i for i in ch_getAppointments(p['links']['self'])['items']]\n",
    "        o['items'] = [i for i in o['items'] if len(i['items'])]\n",
    "    return o"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true,
    "scrolled": false
   },
   "outputs": [],
   "source": [
    "appointments=pd.DataFrame()\n",
    "for c in candidates['candidate'].tolist():\n",
    "    name=c.split()\n",
    "    cand=' '.join(name[1:]+name[0:1])\n",
    "    results=ch_searchOfficers(cand,n=50,exact='fullname')\n",
    "    for result in results['items']:\n",
    "        appointments=pd.concat([appointments,pd.DataFrame.from_dict([result])])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>address</th>\n",
       "      <th>address_snippet</th>\n",
       "      <th>appointment_count</th>\n",
       "      <th>date_of_birth</th>\n",
       "      <th>description</th>\n",
       "      <th>description_identifiers</th>\n",
       "      <th>kind</th>\n",
       "      <th>links</th>\n",
       "      <th>matches</th>\n",
       "      <th>snippet</th>\n",
       "      <th>title</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>{u'country': u'PE38 0JN', u'region': u'Norfolk...</td>\n",
       "      <td>Holly House, Ely Road Hilgay, Downham Market, ...</td>\n",
       "      <td>4</td>\n",
       "      <td>{u'year': 1964, u'month': 4}</td>\n",
       "      <td>Total number of appointments 4 - Born April 1964</td>\n",
       "      <td>[appointment-count, born-on]</td>\n",
       "      <td>searchresults#officer</td>\n",
       "      <td>{u'self': u'/officers/P3V_0gkwW7uqr5JfjhoylIRG...</td>\n",
       "      <td>{u'snippet': [], u'title': [1, 11, 13, 16, 18,...</td>\n",
       "      <td></td>\n",
       "      <td>Christopher John BROWN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>{u'locality': u'Norwich', u'premises': u'21', ...</td>\n",
       "      <td>21 Springfields, Poringland, Norwich, Norfolk,...</td>\n",
       "      <td>2</td>\n",
       "      <td>{u'year': 1968, u'month': 9}</td>\n",
       "      <td>Total number of appointments 2 - Born Septembe...</td>\n",
       "      <td>[appointment-count, born-on]</td>\n",
       "      <td>searchresults#officer</td>\n",
       "      <td>{u'self': u'/officers/TL0ksAgMupTuLf8CHv1dwcUB...</td>\n",
       "      <td>{u'snippet': [], u'title': [1, 6, 8, 16, 18, 23]}</td>\n",
       "      <td></td>\n",
       "      <td>Nicola Jeannette FOWLER</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>{u'locality': u'Harleston', u'premises': u'Off...</td>\n",
       "      <td>Office Number One First Floor Offices, Memoria...</td>\n",
       "      <td>1</td>\n",
       "      <td>{u'year': 1951, u'month': 12}</td>\n",
       "      <td>Total number of appointments 1 - Born December...</td>\n",
       "      <td>[appointment-count, born-on]</td>\n",
       "      <td>searchresults#officer</td>\n",
       "      <td>{u'self': u'/officers/U7wK3BHRf8fK2JJUk9xkqm-G...</td>\n",
       "      <td>{u'snippet': [], u'title': [1, 6, 8, 12, 14, 18]}</td>\n",
       "      <td></td>\n",
       "      <td>Martin James WILBY</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>{u'locality': u'Norwich', u'premises': u'1', u...</td>\n",
       "      <td>1 Middleton Street, Wymondham, Norwich, Norfol...</td>\n",
       "      <td>2</td>\n",
       "      <td>{u'month': 7, u'year': 1944}</td>\n",
       "      <td>Total number of appointments 2 - Born July 1944</td>\n",
       "      <td>[appointment-count, born-on]</td>\n",
       "      <td>searchresults#officer</td>\n",
       "      <td>{u'self': u'/officers/vuhGJ1vGf7rPTPHrW6oG-8vp...</td>\n",
       "      <td>{u'snippet': [], u'title': [1, 5, 7, 11, 13, 19]}</td>\n",
       "      <td></td>\n",
       "      <td>Colin Wayne FOULGER</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>{u'country': u'NR14 8AL', u'region': u'Norfolk...</td>\n",
       "      <td>Medway, The Rosery Mulbarton, Norwich, Norfolk...</td>\n",
       "      <td>0</td>\n",
       "      <td>{u'year': 1957, u'month': 5}</td>\n",
       "      <td>Total number of appointments 0 - Born May 1957</td>\n",
       "      <td>[appointment-count, born-on]</td>\n",
       "      <td>searchresults#officer</td>\n",
       "      <td>{u'self': u'/officers/-GPL4ykYfKUTSa2v9JgJZGV8...</td>\n",
       "      <td>{u'snippet': [], u'title': [1, 6, 8, 12, 14, 19]}</td>\n",
       "      <td></td>\n",
       "      <td>Steven Leigh SEWELL</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>{u'premises': u'Shire Hall', u'country': u'NR1...</td>\n",
       "      <td>Shire Hall, Market Avenue, Norwich, Norfolk, N...</td>\n",
       "      <td>3</td>\n",
       "      <td>{u'year': 1950, u'month': 5}</td>\n",
       "      <td>Total number of appointments 3 - Born May 1950</td>\n",
       "      <td>[appointment-count, born-on]</td>\n",
       "      <td>searchresults#officer</td>\n",
       "      <td>{u'self': u'/officers/iVcH6EunMuXWPbRK1GH5CpYf...</td>\n",
       "      <td>{u'snippet': [], u'title': [1, 8, 10, 17]}</td>\n",
       "      <td></td>\n",
       "      <td>Margaret DEWSBURY</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>{u'premises': u'Dragon Hall', u'country': u'NR...</td>\n",
       "      <td>Dragon Hall, 115/123 King Street, Norwich, Nor...</td>\n",
       "      <td>0</td>\n",
       "      <td>{u'year': 1947, u'month': 3}</td>\n",
       "      <td>Total number of appointments 0 - Born March 1947</td>\n",
       "      <td>[appointment-count, born-on]</td>\n",
       "      <td>searchresults#officer</td>\n",
       "      <td>{u'self': u'/officers/FJef2bYUqPqvbSUWJnSRDEFJ...</td>\n",
       "      <td>{u'snippet': [], u'title': [1, 5, 7, 12, 14, 22]}</td>\n",
       "      <td></td>\n",
       "      <td>David George BISSONNET</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>{u'locality': u'Norwich', u'premises': u'25', ...</td>\n",
       "      <td>25 Field Lane, Hempnall, Norwich, Norfolk, Eng...</td>\n",
       "      <td>1</td>\n",
       "      <td>{u'year': 1949, u'month': 6}</td>\n",
       "      <td>Total number of appointments 1 - Born June 1949</td>\n",
       "      <td>[appointment-count, born-on]</td>\n",
       "      <td>searchresults#officer</td>\n",
       "      <td>{u'self': u'/officers/y98lznNgBxCMZkhX20ajblyq...</td>\n",
       "      <td>{u'snippet': [], u'title': [1, 5, 7, 13, 15, 19]}</td>\n",
       "      <td></td>\n",
       "      <td>Barry Michael STONE</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>{u'locality': u'Great Yarmouth', u'premises': ...</td>\n",
       "      <td>35 Clover Way, Bradwell, Great Yarmouth, Norfo...</td>\n",
       "      <td>7</td>\n",
       "      <td>{u'year': 1949, u'month': 6}</td>\n",
       "      <td>Total number of appointments 7 - Born June 1949</td>\n",
       "      <td>[appointment-count, born-on]</td>\n",
       "      <td>searchresults#officer</td>\n",
       "      <td>{u'self': u'/officers/7OzEbU9cwaUT9OpeWYKzRswf...</td>\n",
       "      <td>{u'snippet': [], u'title': [1, 5, 7, 13, 15, 19]}</td>\n",
       "      <td></td>\n",
       "      <td>Barry Michael STONE</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>{u'country': u'NR16 1EQ', u'region': u'Norfolk...</td>\n",
       "      <td>The Barn Rattees Corner, Fundenhall, Norwich, ...</td>\n",
       "      <td>1</td>\n",
       "      <td>{u'year': 1946, u'month': 9}</td>\n",
       "      <td>Total number of appointments 1 - Born Septembe...</td>\n",
       "      <td>[appointment-count, born-on]</td>\n",
       "      <td>searchresults#officer</td>\n",
       "      <td>{u'self': u'/officers/YTp80cvjgThc5CWBd6T-n110...</td>\n",
       "      <td>{u'snippet': [], u'title': [1, 5, 7, 10, 12, 19]}</td>\n",
       "      <td></td>\n",
       "      <td>Roger Neil PERCIVAL</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>{u'locality': u'Wymondham', u'premises': u'Wym...</td>\n",
       "      <td>Wymondham College, Golf Links Road, Morley, Wy...</td>\n",
       "      <td>4</td>\n",
       "      <td>{u'year': 1961, u'month': 12}</td>\n",
       "      <td>Total number of appointments 4 - Born December...</td>\n",
       "      <td>[appointment-count, born-on]</td>\n",
       "      <td>searchresults#officer</td>\n",
       "      <td>{u'self': u'/officers/5nNHBr0osJASt981ieIgtgVX...</td>\n",
       "      <td>{u'snippet': [], u'title': [1, 6, 8, 11, 13, 18]}</td>\n",
       "      <td></td>\n",
       "      <td>Alison Mary THOMAS</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                             address  \\\n",
       "0  {u'country': u'PE38 0JN', u'region': u'Norfolk...   \n",
       "0  {u'locality': u'Norwich', u'premises': u'21', ...   \n",
       "0  {u'locality': u'Harleston', u'premises': u'Off...   \n",
       "0  {u'locality': u'Norwich', u'premises': u'1', u...   \n",
       "0  {u'country': u'NR14 8AL', u'region': u'Norfolk...   \n",
       "0  {u'premises': u'Shire Hall', u'country': u'NR1...   \n",
       "0  {u'premises': u'Dragon Hall', u'country': u'NR...   \n",
       "0  {u'locality': u'Norwich', u'premises': u'25', ...   \n",
       "0  {u'locality': u'Great Yarmouth', u'premises': ...   \n",
       "0  {u'country': u'NR16 1EQ', u'region': u'Norfolk...   \n",
       "0  {u'locality': u'Wymondham', u'premises': u'Wym...   \n",
       "\n",
       "                                     address_snippet  appointment_count  \\\n",
       "0  Holly House, Ely Road Hilgay, Downham Market, ...                  4   \n",
       "0  21 Springfields, Poringland, Norwich, Norfolk,...                  2   \n",
       "0  Office Number One First Floor Offices, Memoria...                  1   \n",
       "0  1 Middleton Street, Wymondham, Norwich, Norfol...                  2   \n",
       "0  Medway, The Rosery Mulbarton, Norwich, Norfolk...                  0   \n",
       "0  Shire Hall, Market Avenue, Norwich, Norfolk, N...                  3   \n",
       "0  Dragon Hall, 115/123 King Street, Norwich, Nor...                  0   \n",
       "0  25 Field Lane, Hempnall, Norwich, Norfolk, Eng...                  1   \n",
       "0  35 Clover Way, Bradwell, Great Yarmouth, Norfo...                  7   \n",
       "0  The Barn Rattees Corner, Fundenhall, Norwich, ...                  1   \n",
       "0  Wymondham College, Golf Links Road, Morley, Wy...                  4   \n",
       "\n",
       "                   date_of_birth  \\\n",
       "0   {u'year': 1964, u'month': 4}   \n",
       "0   {u'year': 1968, u'month': 9}   \n",
       "0  {u'year': 1951, u'month': 12}   \n",
       "0   {u'month': 7, u'year': 1944}   \n",
       "0   {u'year': 1957, u'month': 5}   \n",
       "0   {u'year': 1950, u'month': 5}   \n",
       "0   {u'year': 1947, u'month': 3}   \n",
       "0   {u'year': 1949, u'month': 6}   \n",
       "0   {u'year': 1949, u'month': 6}   \n",
       "0   {u'year': 1946, u'month': 9}   \n",
       "0  {u'year': 1961, u'month': 12}   \n",
       "\n",
       "                                         description  \\\n",
       "0   Total number of appointments 4 - Born April 1964   \n",
       "0  Total number of appointments 2 - Born Septembe...   \n",
       "0  Total number of appointments 1 - Born December...   \n",
       "0    Total number of appointments 2 - Born July 1944   \n",
       "0     Total number of appointments 0 - Born May 1957   \n",
       "0     Total number of appointments 3 - Born May 1950   \n",
       "0   Total number of appointments 0 - Born March 1947   \n",
       "0    Total number of appointments 1 - Born June 1949   \n",
       "0    Total number of appointments 7 - Born June 1949   \n",
       "0  Total number of appointments 1 - Born Septembe...   \n",
       "0  Total number of appointments 4 - Born December...   \n",
       "\n",
       "        description_identifiers                   kind  \\\n",
       "0  [appointment-count, born-on]  searchresults#officer   \n",
       "0  [appointment-count, born-on]  searchresults#officer   \n",
       "0  [appointment-count, born-on]  searchresults#officer   \n",
       "0  [appointment-count, born-on]  searchresults#officer   \n",
       "0  [appointment-count, born-on]  searchresults#officer   \n",
       "0  [appointment-count, born-on]  searchresults#officer   \n",
       "0  [appointment-count, born-on]  searchresults#officer   \n",
       "0  [appointment-count, born-on]  searchresults#officer   \n",
       "0  [appointment-count, born-on]  searchresults#officer   \n",
       "0  [appointment-count, born-on]  searchresults#officer   \n",
       "0  [appointment-count, born-on]  searchresults#officer   \n",
       "\n",
       "                                               links  \\\n",
       "0  {u'self': u'/officers/P3V_0gkwW7uqr5JfjhoylIRG...   \n",
       "0  {u'self': u'/officers/TL0ksAgMupTuLf8CHv1dwcUB...   \n",
       "0  {u'self': u'/officers/U7wK3BHRf8fK2JJUk9xkqm-G...   \n",
       "0  {u'self': u'/officers/vuhGJ1vGf7rPTPHrW6oG-8vp...   \n",
       "0  {u'self': u'/officers/-GPL4ykYfKUTSa2v9JgJZGV8...   \n",
       "0  {u'self': u'/officers/iVcH6EunMuXWPbRK1GH5CpYf...   \n",
       "0  {u'self': u'/officers/FJef2bYUqPqvbSUWJnSRDEFJ...   \n",
       "0  {u'self': u'/officers/y98lznNgBxCMZkhX20ajblyq...   \n",
       "0  {u'self': u'/officers/7OzEbU9cwaUT9OpeWYKzRswf...   \n",
       "0  {u'self': u'/officers/YTp80cvjgThc5CWBd6T-n110...   \n",
       "0  {u'self': u'/officers/5nNHBr0osJASt981ieIgtgVX...   \n",
       "\n",
       "                                             matches snippet  \\\n",
       "0  {u'snippet': [], u'title': [1, 11, 13, 16, 18,...           \n",
       "0  {u'snippet': [], u'title': [1, 6, 8, 16, 18, 23]}           \n",
       "0  {u'snippet': [], u'title': [1, 6, 8, 12, 14, 18]}           \n",
       "0  {u'snippet': [], u'title': [1, 5, 7, 11, 13, 19]}           \n",
       "0  {u'snippet': [], u'title': [1, 6, 8, 12, 14, 19]}           \n",
       "0         {u'snippet': [], u'title': [1, 8, 10, 17]}           \n",
       "0  {u'snippet': [], u'title': [1, 5, 7, 12, 14, 22]}           \n",
       "0  {u'snippet': [], u'title': [1, 5, 7, 13, 15, 19]}           \n",
       "0  {u'snippet': [], u'title': [1, 5, 7, 13, 15, 19]}           \n",
       "0  {u'snippet': [], u'title': [1, 5, 7, 10, 12, 19]}           \n",
       "0  {u'snippet': [], u'title': [1, 6, 8, 11, 13, 18]}           \n",
       "\n",
       "                     title  \n",
       "0   Christopher John BROWN  \n",
       "0  Nicola Jeannette FOWLER  \n",
       "0       Martin James WILBY  \n",
       "0      Colin Wayne FOULGER  \n",
       "0      Steven Leigh SEWELL  \n",
       "0        Margaret DEWSBURY  \n",
       "0   David George BISSONNET  \n",
       "0      Barry Michael STONE  \n",
       "0      Barry Michael STONE  \n",
       "0      Roger Neil PERCIVAL  \n",
       "0       Alison Mary THOMAS  "
      ]
     },
     "execution_count": 44,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "appointments[appointments['address_snippet'].str.contains(localarea)]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "companies=pd.DataFrame()\n",
    "localAppointments=appointments[appointments['address_snippet'].str.contains(localarea)]\n",
    "for appointment in localAppointments['links'].apply(pd.Series)['self'].tolist():\n",
    "    ddx=pd.DataFrame.from_dict(ch_getAppointments(appointment)['items'])\n",
    "    tmp=pd.concat([ddx.drop(['appointed_to','name_elements','links','address'], axis=1),\n",
    "                   ddx['appointed_to'].apply(pd.Series),ddx['address'].apply(pd.Series)], axis=1)\n",
    "    companies=pd.concat([companies,tmp])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>name</th>\n",
       "      <th>company_status</th>\n",
       "      <th>company_number</th>\n",
       "      <th>company_name</th>\n",
       "      <th>appointed_on</th>\n",
       "      <th>resigned_on</th>\n",
       "      <th>address_snippet</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Christopher John BROWN</td>\n",
       "      <td>active</td>\n",
       "      <td>05491209</td>\n",
       "      <td>CHRIS BROWN (DOWNHAM MARKET) LIMITED</td>\n",
       "      <td>2005-06-27</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Holly House, Ely Road Hilgay, Downham Market, ...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Christopher John BROWN</td>\n",
       "      <td>active</td>\n",
       "      <td>03258034</td>\n",
       "      <td>ARTEK-DESIGN-HOUSE LIMITED</td>\n",
       "      <td>1997-06-17</td>\n",
       "      <td>2005-04-30</td>\n",
       "      <td>Holly House, Ely Road Hilgay, Downham Market, ...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Christopher John BROWN</td>\n",
       "      <td>active</td>\n",
       "      <td>02351921</td>\n",
       "      <td>BROWN CONSULTING SERVICES LIMITED</td>\n",
       "      <td>1997-05-06</td>\n",
       "      <td>1997-06-18</td>\n",
       "      <td>Holly House, Ely Road Hilgay, Downham Market, ...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Christopher John BROWN</td>\n",
       "      <td>active</td>\n",
       "      <td>03258034</td>\n",
       "      <td>ARTEK-DESIGN-HOUSE LIMITED</td>\n",
       "      <td>1996-10-02</td>\n",
       "      <td>1997-06-16</td>\n",
       "      <td>Holly House, Ely Road Hilgay, Downham Market, ...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Nicola Jeannette FOWLER</td>\n",
       "      <td>active</td>\n",
       "      <td>10032213</td>\n",
       "      <td>NJF CONNECTIONS LIMITED</td>\n",
       "      <td>2016-02-29</td>\n",
       "      <td>NaN</td>\n",
       "      <td>21 Springfields, Poringland, Norwich, Norfolk,...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                      name company_status company_number  \\\n",
       "0   Christopher John BROWN         active       05491209   \n",
       "1   Christopher John BROWN         active       03258034   \n",
       "2   Christopher John BROWN         active       02351921   \n",
       "3   Christopher John BROWN         active       03258034   \n",
       "4  Nicola Jeannette FOWLER         active       10032213   \n",
       "\n",
       "                           company_name appointed_on resigned_on  \\\n",
       "0  CHRIS BROWN (DOWNHAM MARKET) LIMITED   2005-06-27         NaN   \n",
       "1            ARTEK-DESIGN-HOUSE LIMITED   1997-06-17  2005-04-30   \n",
       "2     BROWN CONSULTING SERVICES LIMITED   1997-05-06  1997-06-18   \n",
       "3            ARTEK-DESIGN-HOUSE LIMITED   1996-10-02  1997-06-16   \n",
       "4               NJF CONNECTIONS LIMITED   2016-02-29         NaN   \n",
       "\n",
       "                                     address_snippet  \n",
       "0  Holly House, Ely Road Hilgay, Downham Market, ...  \n",
       "1  Holly House, Ely Road Hilgay, Downham Market, ...  \n",
       "2  Holly House, Ely Road Hilgay, Downham Market, ...  \n",
       "3  Holly House, Ely Road Hilgay, Downham Market, ...  \n",
       "4  21 Springfields, Poringland, Norwich, Norfolk,...  "
      ]
     },
     "execution_count": 46,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "corecols=['name','company_status','company_number','company_name','appointed_on','resigned_on']\n",
    "\n",
    "localcos=companies[corecols].reset_index(drop=True)\n",
    "localcos=localAppointments[['title','address_snippet']].merge(localcos, left_on='title',right_on='name')[corecols+['address_snippet']]\n",
    "localcos.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "metadata": {
    "collapsed": false,
    "deletable": true,
    "editable": true
   },
   "outputs": [],
   "source": [
    "#Save company data file\n",
    "localcos.to_csv(companiesfilename,index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 2",
   "language": "python",
   "name": "python2"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
