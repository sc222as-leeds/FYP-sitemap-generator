from flask import render_template, redirect, url_for, request
from app import app
from .forms import WebsiteForm
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import queue
import time
import json
import re

start_time = time.time()

class Node:
    def __init__(self, parent, url, neighbour_nodes):
        self.parent = parent
        self.url = url
        self.neighbour_nodes = neighbour_nodes

    def dict(self):
        return {
            "parent" : self.parent,
            "url" : self.url,
            "neighbour_nodes" : self.neighbour_nodes
        }

class Graph:
    def __init__(self, root):
        self.nodes_queue = queue.Queue()
        self.discovered_nodes = {}
        self.root = root

    def dict(self):
        return {
            "root" : self.root.dict(),
            "discovered_nodes" : { url : node.dict() for url, node in self.discovered_nodes.items() }
        }

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

    root = Node("", url, [])

    graph = Graph(root)

    graph.discovered_nodes[root.url] = root

    string = root.url + ":"

    string = Search(graph, root, string, 0, root, 3)

    grap_data = graph.dict()

    return render_template('result.html',
                    title='Result',
                    graph_json=json.dumps(grap_data),
                    graph=graph)

def Search(graph, current_node, string, depth, parent, max_depth):
    global start_time
    url = current_node.url

    if current_node.parent != parent:
        parent = current_node.parent
        depth += 1

    if depth > max_depth:
        return string

    Wait(6) # wait 6 seconds before next call

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Get the source code
        html = response.text

        start_time = time.time()

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

                node = Node(current_node.url, full_url, [])

                parsed_url = urlparse(full_url)

                if parsed_url.path and full_url not in graph.discovered_nodes:
                    graph.nodes_queue.put(node)
                    graph.discovered_nodes[full_url] = node

        current_node.neighbour_nodes = results

        string += str(results) + "\n"
    except requests.RequestException as e:
        string += "[]\n"

    if not graph.nodes_queue.empty():
        next_node = graph.nodes_queue.get()
        string += next_node.url + ":"
        return Search(graph, next_node, string, depth, parent, max_depth)
    else:
        return string

def ReturnResults(graph):
    string = ""
    for key, element in graph.discovered_nodes:
        string += key + "\n"
    return string

def Wait(delay):
    time_passed = time.time()
    while (time_passed - start_time) < delay:
        time_passed = time.time()
