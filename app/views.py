from flask import render_template, redirect, url_for, request
from app import app
from .forms import WebsiteForm
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import queue
import re

class Graph:
    def __init__(self, root):
        self.nodes_queue = queue.Queue()
        self.discovered_nodes = set()
        self.root = root

class Node:
    def __init__(self, url, neighbour_nodes):
        self.url = url
        self.neighbour_nodes = neighbour_nodes

@app.route('/', methods=['GET', 'POST'])
def index():
    form = WebsiteForm()

    if form.validate_on_submit():
        return redirect(url_for('displayResult', url=form.url.data))
    return render_template('index.html',
                           title='Main Page',
                           form=form)

@app.route('/display-result', methods=['GET', 'POST'])
def displayResult():
    url = request.args.get('url', None)

    root = Node(url, [])

    graph = Graph(root)

    graph.discovered_nodes.add(root.url)

    string = root.url + ":"

    string = Search(graph, root, string)

    return render_template('result.html',
                    title='Result',
                    result=string)

def Search(graph, current_node, string):
    url = current_node.url

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Get the source code
        html = response.text

        # html_no_comments = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

        # href_pattern = r'<a.*href=["\'](.*?)["\']'
        # links = re.findall(href_pattern, html_no_comments)

        soup = BeautifulSoup(html, 'html.parser')

        links = soup.find_all('a', href=True)

        results = []

        for link in links:
            href = link['href']
            if href != "/" and href[0] != "#" and href != "":
                # Use urljoin to handle relative URLs
                full_url = urljoin(url, href)
                results.append(full_url)

                node = Node(full_url, [])

                parsed_url = urlparse(full_url)

                if parsed_url.path and full_url not in graph.discovered_nodes:
                    graph.nodes_queue.put(node)
                    graph.discovered_nodes.add(full_url)

        current_node.neighbour_nodes = results

        string += str(results) + "\n"
    except requests.RequestException as e:
        string += "[]\n"

    if not graph.nodes_queue.empty():
        next_node = graph.nodes_queue.get()
        string += next_node.url + ":"
        return Search(graph, next_node, string)
    else:
        return string

def ReturnResults(graph):
    string = ""
    for element in graph.discovered_nodes:
        string += element + "\n"
    return string
