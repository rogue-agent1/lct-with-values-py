#!/usr/bin/env python3
"""Link-cut tree with path aggregates (max on path)."""

class Node:
    __slots__=("val","mx","ch","p","rev")
    def __init__(self,v):self.val=v;self.mx=v;self.ch=[None,None];self.p=None;self.rev=False
def _is_root(x):return not x.p or(x.p.ch[0]is not x and x.p.ch[1]is not x)
def _push(x):
    if x and x.rev:
        x.ch[0],x.ch[1]=x.ch[1],x.ch[0]
        for c in x.ch:
            if c:c.rev^=True
        x.rev=False
def _pull(x):
    if x:
        x.mx=x.val
        for c in x.ch:
            if c:x.mx=max(x.mx,c.mx)
def _rot(x):
    y=x.p;z=y.p;d=0 if y.ch[1]is x else 1;y.ch[1-d]=x.ch[d]
    if x.ch[d]:x.ch[d].p=y
    x.p=z
    if z:
        if z.ch[0]is y:z.ch[0]=x
        elif z.ch[1]is y:z.ch[1]=x
    x.ch[d]=y;y.p=x;_pull(y);_pull(x)
def _splay(x):
    while not _is_root(x):
        y=x.p
        if not _is_root(y):
            z=y.p;_push(z);_push(y);_push(x)
            if(z.ch[0]is y)==(y.ch[0]is x):_rot(y)
            else:_rot(x)
            _rot(x)
        else:_push(y);_push(x);_rot(x)
    _push(x)
def access(x):
    last=None;u=x
    while u:_splay(u);u.ch[1]=last;_pull(u);last=u;u=u.p
    _splay(x)
def make_root(x):access(x);x.rev^=True;_push(x)
def link(x,y):make_root(x);x.p=y
def cut(x,y):make_root(x);access(y);y.ch[0]=None;x.p=None;_pull(y)
def path_max(x,y):make_root(x);access(y);return y.mx

def main():
    nodes=[Node(i*10) for i in range(5)]
    link(nodes[0],nodes[1]);link(nodes[1],nodes[2]);link(nodes[2],nodes[3]);link(nodes[3],nodes[4])
    print(f"Path max 0-4: {path_max(nodes[0],nodes[4])}")
    print(f"Path max 1-3: {path_max(nodes[1],nodes[3])}")

if __name__=="__main__":main()
