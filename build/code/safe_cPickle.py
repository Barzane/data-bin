# -*- coding: utf-8 -*-

def safe_cPickle_dump(dst, object):

    import cPickle, segment_timer

    try:
        
        file=open(dst, 'r')
        file.close()
        
        rsp = ''
        
        while rsp != 'n' and rsp != 'y':
            rsp = raw_input('(safe_cPickle has detected object "' + dst + '") Overwrite? (y/n) ')
            
        if rsp == 'y':
            
            t_pickle_start = segment_timer.timer(True)
            
            file_ = open(dst, 'wb')
            cPickle.dump(object, file_)
            file_.close()
            
            print '%0.3f seconds to cPickle file'%(segment_timer.timer(False, t_pickle_start))
            print
            
        else:
            raise Exception('terminating')
        
    except IOError:
        
        print '\n' + '(safe_cPickle has not detected object "' + dst + '") Saving object.'
        
        t_pickle_start = segment_timer.timer(True)
        
        file_ = open(dst, 'wb')
        cPickle.dump(object, file_)
        file_.close()
        
        print '%0.3f seconds to cPickle file'%(segment_timer.timer(False, t_pickle_start))
        print
        
    return None
