from database.models import *

caption = []
image = []
data = []

def getDetailsFromSearchToken( token ):
    city = CITY.objects.all()
    for x in city:
        if x.cityName.lower().find( token.lower()) != -1:
            if x.cityName in caption:
                continue
            caption.append( x.cityName )
            image.append( x.image )
            data.append(x.description)
    
    for x in city:
        if x.description.lower().find( token.lower()) != -1:
            if x.cityName in caption:
                continue
            caption.append( x.cityName )
            image.append( x.image )
            data.append(x.description)
    
    spot = SPOT.objects.all()
    for x in spot:
        if x.spotName.lower().find( token.lower()) != -1:
            if x.spotName in caption:
                continue
            caption.append( x.spotName )
            image.append( x.image )
            data.append(x.spotInfo)
    for x in spot:
        if x.spotInfo.lower().find( token.lower()) != -1:
            if x.spotName in caption:
                continue
            caption.append( x.spotName )
            image.append( x.image )
            data.append(x.spotInfo)
    
    blog = BLOG.objects.all()
    for x in blog:
        if x.blogCaption.lower().find( token.lower()) != -1:
            if x.blogCaption in caption:
                continue
            caption.append( x.blogCaption )
            image.append( x.image )
            data.append(x.blogData)

    for x in blog:
        if x.blogData.lower().find( token.lower()) != -1:
            if x.blogCaption in caption:
                continue
            caption.append( x.blogCaption )
            image.append( x.image )
            data.append(x.blogData)

#call this function using the search string user provided
def getDetailsFromSearchKey( key ):    
    caption.clear()
    image.clear()
    data.clear()
    getDetailsFromSearchToken(key)
    tokens = key.split()
    for token in tokens:
        getDetailsFromSearchToken(token)
    ret_caption=caption
    ret_data=data
    ret_image=image
    return (ret_caption, ret_data, ret_image)

#getDetailsFromSearchKey("dHaka")
#print(caption)

