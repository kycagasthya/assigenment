from google.cloud import documentai_v1beta3 as documentai
from google.cloud.documentai_v1beta3.services.document_processor_service.transports.grpc import (DocumentProcessorServiceGrpcTransport)
from google.cloud import storage
import json
import PyPDF2
from io import BytesIO
import img2pdf

# Instantiates a client with max 20MB file
channel = DocumentProcessorServiceGrpcTransport.create_channel(
    options=[("grpc.max_receive_message_length", 20 * 1024 * 1024)])
transport = DocumentProcessorServiceGrpcTransport(channel=channel)
client = documentai.DocumentProcessorServiceClient(transport=transport)

def process_document_sample(
    project_id: str, location: str, processor_id: str, file_path: str
):
    global client
    
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Read the file into memory
    document = {"content": image_content, "mime_type": "application/pdf"}

    # Configure the process request
    request = {"name": name, "document": document}

    # Recognizes text entities in the PDF document
    result = client.process_document(request=request)

    document = result.document
            
    return document

def split_pdf(pdfReader, file_name):
    """
    Todo : update doc string
    """
    start = 0
    end = 5 
    splits = pdfReader.numPages//5
    output_files = []

    for i in range(splits+1): 
        # creating pdf writer object for ith split 
        if start == end: break
        pdfWriter = PyPDF2.PdfFileWriter() 

        # output pdf file name 
        outputpdf = file_name.split('.pdf')[0] + "_" + str(i) + '.pdf'
        output_files.append(outputpdf)

        # adding pages to pdf writer object 
        for page in range(start,end): 
            pdfWriter.addPage(pdfReader.getPage(page)) 

        # writing split pdf pages to pdf file 
        with open(outputpdf, "wb") as f: 
            pdfWriter.write(f) 

        # interchanging page split start position for next split 
        start = end 

        end = end+5
        if end >= pdfReader.numPages:
            end = pdfReader.numPages
    
    return output_files

def pre_process(file_name, file_path, input_bucket, project_id, location, processor_id):    
    #global results
    results = []
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(input_bucket)
    
    # Download pdf file from bucket
    try:
        blob = bucket.blob(file_path)
        blob.download_to_filename(file_name)
    except Exception as e:
        return {"error": e}, {}

    # Read pdf file to check for pages, encryption
    try:
        pdfFileObj = open(file_name, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        number_of_pages = pdfReader.numPages
    except:
        pdfFileObj.close()
        return {"error": "Cannot read file"}, {}

    page_orientations = {}
    
    if number_of_pages > 5:
        # Split pdf in groups of 5 pages
        output_files = split_pdf(pdfReader, file_name)
        page_count = 0

        # Run Form Parser on each group
        for outputpdf in output_files:
            if page_count == 0:
                try:
                    doc = process_document_sample(project_id, location, processor_id, outputpdf)
                    results.append(doc)
                except:
                    pdfFileObj.close()
                    return {"error": "Form Parser API call failed"}, {}


                page_count = len(doc.pages)
            else:
                # for 2nd group onwards, append to 1st group result doc object
                try:
                    doc1 = process_document_sample(project_id, location, processor_id, outputpdf)
                    results.append(doc1)
                except:
                    pdfFileObj.close()
                    return {"error": "Form Parser API call failed"}, {}
                
                page_count_old = page_count
                for page in doc1.pages:
                    page.page_number = page_count+1
                    page_count = page_count+1
                    
                    page_count = page_count_old
                    for page in doc1.pages:
                        page.page_number = page_count+1
                        page_count = page_count+1

                # +1 for \n added after previous text
                text_length = len(doc.text)+1
                
                # Update text anchors of objects
                for page in doc1.pages:
                    for token in page.tokens:
                        token.layout.text_anchor.text_segments[0].start_index = token.layout.text_anchor.text_segments[0].start_index + text_length
                        token.layout.text_anchor.text_segments[0].end_index = token.layout.text_anchor.text_segments[0].end_index + text_length

                doc.pages.extend(doc1.pages)
                doc.text = doc.text + "\n" + doc1.text
    else:
        try:
            doc = process_document_sample(project_id, location, processor_id, file_name)
            results.append(doc)
        except:
            pdfFileObj.close()
            return {"error": "Form Parser API call failed"}, {}


    pdfFileObj.close()
    return doc, page_orientations,results
