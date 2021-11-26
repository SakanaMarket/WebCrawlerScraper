import re
from lxml import html
from lxml.html.clean import Cleaner
from urllib.parse import urlparse
from collections import defaultdict
import json

unique_pages = 0
longest_page = ( "", 0 )
words = defaultdict( int )
subdomains = defaultdict( int )


def scraper(url, resp):
        if resp and resp.raw_response and resp.raw_response.is_redirect:
                resp.raw_response = resp.raw_reponse.history[-1]
                url = resp.raw_response.url
        return extract_next_links(url, resp)

def extract_next_links(url, resp ):
        if resp.status in range(400,609):
                if resp.status == 601:
                        with open("dead.txt", "a") as file:
                                file.write("{}\n".format(url))
                return []
        else:
                global longest_page, unique_pages, words, subdomains
                try:
                        doc = html.fromstring(resp.raw_response.content, base_url=url )
                        doc.make_links_absolute()
                

                        cleaner = Cleaner( style=True, links=True, scripts=True, javascript=True, remove_unknown_tags=True )
                        line_list = [ re.sub(r"\t|\n", "", x.text).strip() for x in cleaner.clean_html( doc ).xpath("//body//*") if x.text ]
                        token_list = [ word.lower() for line in line_list for word in re.findall("[a-zA-z0-9]{3,}", line) if line ]

                        #increases unique page counter
                        unique_pages += 1

                        #finds longest page in terms of number of words
                        length = len( token_list )
                        if length > longest_page[1]:
                                longest_page= ( url, length )

                        #tokenizes and updates word dictionary
                        for word in token_list:
                                words[ word ] += 1

                        #counts number of unique pages per url
                        link_list = list(set( re.sub(r"#.*", "", link) for link in doc.xpath( "//a/@href" ) if is_valid( link )))
                        if re.match(r"(https|http):[/]{2}(.*\.)ics\.uci\.edu(\/.*)?", url ):
                                subdomains[ r"https://" + urlparse(url).netloc ] = len( link_list )
                        with open("logs.txt", "w") as l:
                                l.write("{}\n".format(unique_pages))
                                l.write("{} : {}\n".format(longest_page[0], longest_page[1]))
                        with open("subdomains.txt", "w") as s:
                                json.dump(subdomains, s)
                        with open("words.txt", "w") as w:
                                json.dump(words, w)
                        return link_list
                except:
                        with open("error.txt", "a") as e:
                                e.write("{}\n".format(url))
                        return []

def is_valid(url):
        try:
                parsed = urlparse(url)
                if parsed.scheme not in set(["http", "https"]):
                        return False

                temp_url = (parsed.netloc + parsed.path).lower()
                
                domain = re.match( r"((.*\.)*(ics|informatics|stat|cs)\.uci\.edu(\/.*)?)|(today\.uci\.edu\/department\/information_computer_sciences(\/.*)?)", temp_url )

                black_list = re.match( r"(.*\.)*(metaviz|asterixdb|archive|timesheet|fano|vip)\.ics\.uci\.edu(\/.*)?", temp_url )

                special = re.match( r"www\.(isg|ucf)\.ics\.uci\.edu(\/.*)?|asterix\.ics\.uci\.edu\/fuzzyjoin-mapreduce|dynamo\.ics\.uci\.edu\/(files\/zImage_paapi|changelog.txt)", temp_url)
                
                fuck_wics = re.match( r"(.*)wics\.ics\.uci\.edu\/.*(language.php|recover).*", temp_url)
                
                calendar = re.search(r"[\d]{4}-[\d]{2}-[\d]{2}", parsed.path.lower()) or re.search("[\d]{4}-[\d]{2}", parsed.path.lower())

                alumni = re.match( r"(.*\.)*ics\.uci\.edu\/(community\/alumni\/index\.php\/(hall_of_fame|stayconnected)(.*)?|alumni\/(stayconnect.*|hall_of_fame.*))", temp_url)

                alumni2 = re.match( r"(.*\.)*alumni\.ics\.uci\.edu.*", temp_url)

                swiki = re.match( r"(.*)swiki\.ics\.uci\.edu\/lib\/exe(.*)?", temp_url)

                saotrap = re.match( r"www\.ics\.uci\.edu\/ugrad\/honors\/index.php\/.*", temp_url)

                flamingo = re.match( r"(.*)flamingo\.ics\.uci\.edu\/(\.\_\.DS\_Store|\.DS\_Store|localsearch\/fuzzysearch)", temp_url)

                ## Ded
                ded = re.match( r"(.*)(lolth\.ics\.uci\.edu\/cgi-bin\/cgiwrap\/sudeep\/file_upload\.cgi|cocoa-krispies\.ics\.uci\.edu\/\~paolo\/JuliusC|mapgrid\.ics\.uci\.edu(.*)?)", temp_url)

                

                

                

                file = re.match(
                                r".*\.(css|js|bmp|gif|jpe?g|ico"
                                +r"|png|tiff?|mid|mp2|mp3|mp4"
                                +r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                                +r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                                +r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                                +r"|epub|dll|cnf|tgz|sha1"
                                +r"|thmx|mso|arff|rtf|jar|csv"+r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

                ics_robot_d = re.match(r"(.*\.)*ics\.uci\.edu\/(bin|~mpufal\/.*)", temp_url)
                today_bot_d = re.match(r"today\.uci\.edu\/department\/information_computer_sciences\/.*(calendar|search|\?utm).*", temp_url)
                today_bot_a = re.match(r"today\.uci\.edu\/department\/information_computer_sciences\/.*(calendar\/(ics|xml)|search\/events\.(ics|xml)).*", temp_url)
                stat_robot_d = re.match(r"(.*\.)*stat\.uci\.edu(\/wp-admin\/.*)", temp_url)
                stat_robot_a = re.match(r"(.*\.)*stat\.uci\.edu(\/wp-admin\/admin-ajax.php)", temp_url)
                in4mtx_robot_d = re.match(r"(.*\.)*informatics\.uci\.edu(\/(wp-admin|research)\/.*)", temp_url)
                in4mtx_robot_a = re.match(r"(.*\.)*informatics\.uci\.edu\/(wp-admin\/admin-ajax.php|research\/(labs_centers|areas-of-expertise|example-research-projects|phd-research|past-dissertations|masters-research|undergraduate-research|gifts-grants)\/.*)", temp_url)
                cs_robot_d = re.match(r"(.*\.)*cs\.uci\.edu(\/wp-admin\/.*)", temp_url)
                cs_robot_a = re.match(r"(.*\.)*cs\.uci\.edu(\/wp-admin\/admin-ajax.php)", temp_url)

                ics_robot = not bool(ics_robot_d)
                today_bot = not (bool(today_bot_d) ^ bool(today_bot_a))
                stat_robot = not (bool(stat_robot_d) ^ bool(stat_robot_d))
                in4mtx_robot = not (bool(in4mtx_robot_d) ^ bool(in4mtx_robot_a))
                cs_robot = not (bool(cs_robot_d) ^ bool(cs_robot_a))

                if domain and not ( file or black_list or special or fuck_wics or calendar or alumni or alumni2 or swiki or saotrap or flamingo or ded):
                        if ics_robot and today_bot and stat_robot and in4mtx_robot and cs_robot:
                                return url

        except TypeError:
                print ("TypeError for ", parsed)
                raise
