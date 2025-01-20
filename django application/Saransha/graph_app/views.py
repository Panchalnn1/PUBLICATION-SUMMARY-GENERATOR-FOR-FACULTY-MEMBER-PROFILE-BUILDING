# graph_app/views.py
import pandas as pd
import matplotlib.pyplot as plt
import io
import  base64
from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')
from django.conf import settings
from Saransha.utils import generate_author_summary,generate_publication_summary
from django.core.files.storage import FileSystemStorage

def dynamic_graph_view(request):
    # First Graph: Journal and Conference Count by Author
    fs = FileSystemStorage()
    output_file_path = fs.path("output.xlsx")
    print(output_file_path)
    if fs.exists(output_file_path): 
        main = pd.read_excel(output_file_path)
    summary= generate_author_summary(main)
    summary1 = summary.drop(columns=["total_citations"])
    df = summary1
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(df['Main Author']))
    ax1.bar(index, df['journal'], bar_width, label='Journal', color='blue')
    ax1.bar([i + bar_width for i in index], df['publication'], bar_width, label='Conference', color='orange')
    ax1.set_xlabel('Main Author')
    ax1.set_ylabel('Count')
    ax1.set_title('Journal and Conference Count by Author')
    ax1.set_xticks([i + bar_width / 2 for i in index])
    ax1.set_xticklabels(df['Main Author'], rotation=45, ha='right')
    ax1.legend()
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    graph1 = base64.b64encode(buf1.getvalue()).decode('utf-8')
    buf1.close()



    # Second Graph: Publications by Author Over Time
    x,y=generate_publication_summary(main)
    years = x
    publications = y
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    bar_width = 0.25
    index = range(len(years))
    for i, (author, counts) in enumerate(publications.items()):
        ax2.bar([x + i * bar_width for x in index], counts, bar_width, label=author)
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Number of Publications')
    ax2.set_title('Publications by Author Over Time')
    ax2.set_xticks([x + bar_width for x in index])
    ax2.set_xticklabels(years, rotation=45, ha='right')
    ax2.legend()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    graph2 = base64.b64encode(buf2.getvalue()).decode('utf-8')
    buf2.close()




    
    summary2 = summary.drop(columns=["journal","total_citations"])
    print(summary2)
    df = summary2
    # Plotting the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df['Main Author'], df['publication'], color='steelblue')
    # Customizing the chart
    ax.set_xlabel('Main Author')
    ax.set_ylabel('Number of Titles')
    ax.set_title('Publication Count by Author')
    plt.xticks(rotation=45, ha='right')
    # Save the plot to a string buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    # Encode the image to a base64 string
    graph3 = base64.b64encode(image_png).decode('utf-8')
    buf1.close()
    

    return render(request, 'graph_app/dynamic_graph.html', {'graph1': graph1, 'graph2': graph2,'graph3': graph3})

       
    
