from flask import Flask, render_template, request, url_for, redirect

from model import GraphDemoModel
from algorithms import topoSort, mermaidSort, dataTablePaths, spanTree

app = Flask(__name__)

@app.route('/index/')
@app.route('/')
def index():
  return render_template("index.html")

@app.route('/graph/', methods=["GET", "POST"])
def graph():
  if request.method == "POST":
    input = request.form["input"]
    start_label = request.form["start_label"]
    command = request.form["command"]
    
    gm = GraphDemoModel()
    gm.createGraph(input, start_label)
    # graph = gm.getGraph()
    
    
    if command == "graph":
      graph = gm._graph.mermaidGraph()
      return render_template("graph.html", result = graph, input=input, start_label = start_label)

    if command == "sort":
      sorted =  " ".join(map(str, gm.run(topoSort)))
      sorted = mermaidSort(sorted)
      return render_template("sort.html", result = sorted, input = input, start_label=start_label)

    if command == "shortest_path":
      paths = dataTablePaths(gm._graph, start_label)
      v_count = len(gm._graph)
      return render_template("shortest_path.html", result = paths, v_count = v_count, input=input, start_label=start_label, graph=graph)

    if command == "span":
      span = " ".join(map(str, gm.run(spanTree)))
      gm2 = GraphDemoModel()
      gm2.createGraph(span,start_label)
      graph2 = gm2._graph.mermaidGraph()
      return render_template("span.html", span=graph2, input=input, start_label=start_label)


app.run(host='0.0.0.0', port=81, debug=True)
