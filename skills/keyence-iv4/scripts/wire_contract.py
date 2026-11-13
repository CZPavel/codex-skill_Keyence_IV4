"""Small offline wire-contract examples. No sockets or device operations.

Supports CR-framed text and OF00 Standard/Sorting only. BR and other result formats
require separate explicit parsers. Limits are application choices, not vendor limits.
"""
import json
import re

class CRFrames:
    def __init__(self, max_buffer=65536):
        if max_buffer < 1: raise ValueError('Positive application buffer limit required')
        self.pending = bytearray(); self.max_buffer = max_buffer
    def feed(self, data):
        if not isinstance(data, bytes): raise TypeError('Pass raw bytes')
        self.pending.extend(data)
        if self.pending[:3].lower() == b'br,':
            self.pending.clear()
            raise ValueError('BR binary image response needs a length-aware parser')
        if len(self.pending) > self.max_buffer:
            self.pending.clear(); raise ValueError('Application buffer limit exceeded')
        result=[]
        while b'\r' in self.pending:
            end=self.pending.index(13); frame=bytes(self.pending[:end+1]); del self.pending[:end+1]
            if frame[:3].lower()==b'br,':
                self.pending.clear(); raise ValueError('BR is not CR-framed ASCII data')
            if b'\n' in frame: raise ValueError('Unexpected LF; CRLF contract not established')
            result.append(frame)
        return result

def parse_error(frame):
    match=re.fullmatch(rb'ER,([^,\r]{1,18}),(\d{2})\r',frame)
    if not match: raise ValueError('Expected ER,command,bb + CR')
    code=match[2].decode('ascii')
    return {'command':match[1].decode('ascii'),'protocol_error':code,
            'meaning':{'02':'unknown command','03':'invalid state or settings','22':'parameter count or range'}.get(code,'unmapped; consult exact source')}

def parse_rt_standard(frame, *, mode, output_format='00'):
    if mode not in ('standard','sorting') or output_format!='00':
        raise ValueError('This example supports only OF00 Standard/Sorting, not detailed/coordinate/count')
    if not frame.endswith(b'\r') or b'\n' in frame: raise ValueError('Expected exact CR terminator')
    fields=frame[:-1].decode('ascii').split(',')
    if len(fields)<6 or fields[0]!='RT' or (len(fields)-3)%3: raise ValueError('Invalid standard RT field groups')
    if not re.fullmatch(r'\d{5}',fields[1]) or int(fields[1])>32767: raise ValueError('Result counter must be 00000..32767')
    allowed={'OK','NG','--',*(f'{n:02d}' for n in range(8))}
    if fields[2] not in ({'OK','NG','--'} if mode=='standard' else {'NG','--',*(f'{n:02d}' for n in range(8))}): raise ValueError('Unknown status for this contract')
    tools=[];seen=set()
    for i in range(3,len(fields),3):
        number,status,score=fields[i:i+3]
        if not re.fullmatch(r'\d{2}',number) or int(number)>(64 if mode=='standard' else 8): raise ValueError('Tool number outside contract')
        if number in seen: raise ValueError('Duplicate tool number')
        seen.add(number)
        if status not in allowed or not re.fullmatch(r'\d{7}',score): raise ValueError('Invalid tool fields')
        tools.append({'number':int(number),'status':status,'raw_value':score,'decidable':status!='--'})
    return {'counter':int(fields[1]),'total':fields[2],'tools':tools,'decidable':fields[2]!='--' and all(t['decidable'] for t in tools),
            'note':'Freshness, physical cycle and units are not determined by this parser.'}

def counter_relation(previous,current,*,same_session=False):
    if not 0<=previous<=32767 or not 0<=current<=32767: raise ValueError('Counter range')
    if not same_session:return {'classification':'unknown','reason':'No continuity across session/restart established'}
    delta=(current-previous)%32768
    return {'classification':'same' if delta==0 else 'next' if delta==1 else 'gap_or_ambiguous','modulo_delta':delta,
            'note':'INFERRED host comparison; not globally unique part identity or exactly-once proof.'}

if __name__=='__main__':
    buffer=CRFrames();frames=buffer.feed(b'T1\rRT,00031,OK,01,OK,0000091\r')
    print(json.dumps({'frames':len(frames),'ack_is_result':False,'result':parse_rt_standard(frames[1],mode='standard')},ensure_ascii=False))
