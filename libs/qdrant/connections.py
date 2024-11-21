#Qdrant 
from qdrant_client.http.models import PointStruct   
from qdrant_client.models import Distance, VectorParams
from qdrant_client import QdrantClient


#fFasrembed embedding
from fastembed.embedding import FlagEmbedding as Embedding
embeded_text = Embedding()


# secrets imports 
from settings import *

#Imports
from langchain.text_splitter import CharacterTextSplitter

import uuid
from settings import *




#create new cluster in Qdrant
record=0


URL="https://36f9a654-1274-472a-bca9-6284d3940e1c.us-east4-0.gcp.cloud.qdrant.io"
QUDRANT_KEY=""
connection = QdrantClient(
    url=URL,  # Use the local server URL
    api_key=QUDRANT_KEY  # Provide your Qdrant API key if required
)



# class multiple_collection :

#     """
#     """

#     def __init__(self):
#         self.embedding_model = Embedding()

#     def recreate_collection(self,document_name:str)->None:
#         connection.recreate_collection(
#             collection_name=document_name,
#             vectors_config=VectorParams(size=384, distance=Distance.COSINE),
#         )
      



#     def get_text_chunks(self,text:str):
#         text_splitter= CharacterTextSplitter(
#             separator="*",
#             chunk_size= 10,
#             chunk_overlap=2
#             # length_function=len
#         )

#         chunks= text_splitter.split_text(text)
#         print("Chunks created")
#         return chunks
    

#     def get_embedding(self,text_chunks,model_id:str="text-embedding-3-small"):
#         points=[]
#         for idx, chunk in enumerate(text_chunks):
#             # response = client.embeddings.create(
#             #     input=[chunk],
#             #     model=model_id
#             # )
#             # embeddings= response.data[0].embedding
#             embeddings = self.embedding_model.embed([chunk])
#             for embedding in embeddings:
#                 embeddings = embedding
#             point_id= str(uuid.uuid4())  #generate a unique id for the point

#             points.append(PointStruct(id=point_id,vector=embeddings,payload={"text":chunk}))
#             print(f"embeddings created")

#         return points
    

#     def insert_data(self,get_points,document_name:str):
#         operation_info= connection.upsert(
#             collection_name=document_name,
#             wait=True,
#             points=get_points
#         )
     


#     def main(self,document_name:str,text_data:str):

#         # try:
#             print(1)
#             self.recreate_collection(document_name)
#             print(2)
#             chunks= self.get_text_chunks(text_data)
#             print(3)
#             vectors=self.get_embedding(chunks)
#             print(4)
#             self.insert_data(vectors,document_name)
#             print(5)


#             return {"success" : True}
#         except:
#             return {"success" : False}
       

# obj_multiple_collection = multiple_collection()



collection_name='dummy-data'

## Storing Data in VD


# resp = obj_multiple_collection.main(collection_name,DUMMY_TEXT)
# print(resp)




## Querying Data From VD


query='reset password'

embedding_model = Embedding()


# Fastembed embedding 

embeddings = embedding_model.embed([query])
for embedding in embeddings:
    embeddings = embedding


search_result = connection.search(
    collection_name=collection_name,
    query_vector=embeddings,
    limit=1)

print(search_result)









# class Vector_Database_utils_funtion:

#     """ 
#     Get All collection id that are present in vector database
#     """

#     def __init__(self) -> None:
#         pass
    
    
#     def get_collections_list(self) -> list:
#         try :
#             collections = list(connection.get_collections())[0][1]
#             collections_list =[]
#             for i in collections:
#                 collections_list.append(i.name)
        
#             return collections_list
#         except Exception as e:
#             logger.error(f"([{__class__.__name__}] {Logger.FUNC_NAME()}) ERROR OCCURRED: {str(e)}")
#             return []
    
#     def delete_collection(self,collection_id:str) -> bool:

#         try :
#             logger.info(f"([{__class__.__name__}] ({Logger.FUNC_NAME()}) collection id for delete: {collection_id} ")
#             response = connection.delete_collection(collection_name=collection_id)
#             # logger.info(f"([{__class__.__name__}] ({Logger.FUNC_NAME()}) collection id {collection_id} successfully deleted")
#             logger.info(f"([{__class__.__name__}] ({Logger.FUNC_NAME()}) Response from qdrant {response}")
#             return response

#         except Exception as e:
#             logger.error(f"[{__class__.__name__}] ({Logger.FUNC_NAME()}) ERROR OCCURRED: {str(e)}")
#             return False


#     def verify_collections(self, collection_id: str) -> bool:

#         collection_list =self.get_collections_list()
#         logger.info(f"({Logger.FUNC_NAME()}) Vector collection list: {collection_list} ")

#         # for collection in collection_names:
                
#         if  collection_id not in collection_list:
#             logger.info(f"([{__class__.__name__}] ({Logger.FUNC_NAME()}) collection id: {collection_id} ")
#             return False 
            
#         return True
  

# obj_Vector_Database_utils_funtion = Vector_Database_utils_funtion()