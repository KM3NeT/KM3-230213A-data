import gzip
import json
from types import SimpleNamespace
import vector
import collections
import copy

def read_zipped_json( zippedfile):

    "read json input file"

    with gzip.open( zippedfile ) as f :
        data = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    
        vector.make_vecs(data)
        if hasattr(data, 'hits') : time_sort_hits(data.hits)
       
        if hasattr(data, 'reconstructed_track') : 
          
            # add 5 ns to the track time to account for the fact that the pdfs used
            # in the reconstruction tend to peak a little bit later than 0, 
            # resulting in a time shift of about 5 ns

            data.reconstructed_track.t += 5 

        return data
    

def ntrig_pmts ( evt ) :
   "return the number of triggered PMTs in the event"
   
   return len( { (h.dom_id, h.channel_id) for h in evt.hits if h.triggered} )


def time_sort_hits( histlist ) : 
   
    return histlist.sort( key = lambda h: h.t )


def bunches( hitslist ) :

    "if hits are separated by 255 ns, they are in the same bunch"

    addnext, prev, r  = True, None, []

    for h in hitslist :

        # add the hit to the bunch if it is the first hit or the time difference is 
        # exactly 255 ns

        addthis = addnext and ( len(r) == 0 or h.tdc - r[-1].tdc == 255 )

        if not addthis : # the bunch ends here
            if r : yield r
            r = []

        r.append( h )
            
        if h.tot == 255 :
            addnext = True
           
    yield r


def summarize( bunch ) :

    "return a single, mergerd, hit from a bunch of hits"

    h0 = copy.copy(bunch[0])
    for i in range (1, len(bunch)) :
        h0.tot += bunch[i].tot

    return h0


def merge_multi_hits( evt ) :

    'replace evt.hits with a list of hits where multiple consequitive hits are merged into a single hit'

    dst = []
    n0 = len( evt.hits )

    M = collections.defaultdict( list )

    for hit in evt.hits :
        M[ (hit.dom_id, hit.channel_id) ].append( hit )

    for pmtid, hitlist in M.items() :
        hitlist.sort( key = lambda h : h.t )

        for bunch in bunches( hitlist ) :
            h = summarize( bunch) 
            dst.append( h )

    evt.hits = dst

    print ( "original hits", n0 )
    print ( "merged hits", len(evt.hits) )
