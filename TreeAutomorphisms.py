from manim import *
import networkx as nx
import itertools

def all_strings(A,n):
    return [''.join(x) for x in itertools.product('012', repeat=n)]

def x(s):
    if len(s)==0:
        return ""
    elif len(s)==1:
        if s == "0": return "1"
        if s == "1": return "0"
        if s == "2": return "2"
    else:
        s0 = s[0]
        if s0 == "0":
            return "1" + s[1:]
        elif s0 == "1":
            return "0" + x(s[1:])
        elif s0 == "2":
            return s

def y(s):
    if len(s)==0:
        return ""
    elif len(s)==1:
        if s == "0": return "2"
        if s == "1": return "1"
        if s == "2": return "0"
    else:
        s0 = s[0]
        if s0 == "0":
            return "2" + s[1:]
        elif s0 == "1":
            return s
        elif s0 == "2":
            return "0" + y(s[1:])

def partial_perm(p,s,n): # will apply permutation up to n characters in
    if n >= len(s):
        return p(s)
    else:
        return p(s)[:n] + s[n:]

class Tree(Graph):
    def __init__(self, alphabet_size=3, depth=2, width=3, **kwargs):
        A = list(range(alphabet_size))
        G = nx.Graph()
        G.add_node("")
        tree_layout = {"":[width/2,0,0]}

        for d in range(1,depth+1):
            for i,s in enumerate(all_strings(A,d)):
                G.add_node(s)
                G.add_edge(s[:-1],s)
                tree_layout[s] = [width*(2*i+1)/(2*alphabet_size**d),-1.5*d,0]

        super().__init__( list(G.nodes), list(G.edges), layout=tree_layout, **kwargs )
        self.center()
    
    def apply_permutation(self, p):
        # new_layout = {"":[self.tree_width/2,0,0]}
        # for d in range(1,self.tree_depth+1):
        #     for i,s in enumerate(all_strings(list(range(self.alphabet_size)),d)):
        #         new_layout[s] = [self.tree_width*(2*i+1)/(2*self.alphabet_size**d),-1*d,0]
        new_layout = {v : self[p(v)].get_center() for v in self.vertices}
        self.change_layout(new_layout)

def TreePermutation(top_permutation, future_permutations):
    # top is a simple bijection from A to A in the form of a shuffled string, future is |A|-tuple of more bijections.
    # Often will be self-referential, that has to be allowed.
    def function(s):
        if len(s)==0:
            return ""
        elif len(s)==1:
            return top_permutation[int(s[0])]
        else:
            chosen_future = future_permutations[int(s[0])]
            if chosen_future==1:
                return top_permutation[int(s[0])] + s[1:]
            else:
                return top_permutation[int(s[0])] + chosen_future(s[1:])
    return function

# x = TreePermutation( "102", (1,x,1) )
# y = TreePermutation( "021", (1,1,y) )


class Generated(Scene):
    def construct(self):
        self.apply_permutation_sequence( [x,y,x,y,x,y,x], ["x","y","x","y","x","y","x"], "1011" )
        
    def apply_permutation(self,p,s):
        G = Tree(3, 4, width=13.5, vertex_config={s : {"fill_color": RED}} )

        string_eq = MathTex( "x(", s, ")", "=", p(s) ).to_edge(DOWN)


        self.add(G)
        self.play(FadeIn(string_eq[:3]))
        self.wait()
        self.play(G.animate.change_layout(layout={v : G[p(v)].get_center() for v in G.vertices}), run_time=5)
        self.play(FadeIn(string_eq[3:]))
        self.wait()
        self.clear()
        # self.play(G.animate.change_layout(layout={v : G[p(v)].get_center() for v in G.vertices}), run_time=1)
        # self.wait()
    
    def staggered_permutation(self,p,p_name,s):
        G = Tree(3, len(s), width=13.5, vertex_config={s : {"fill_color": RED}} ).to_edge(UP)
        G_original = G.copy()

        string_eq = MathTex( p_name, "(", s, ")", "=", p(s) ).to_edge(DOWN)

        self.add(G)
        self.play(Write(string_eq[:4]))
        self.wait()
        for n in range(1,len(s)+1):
            self.play(G.animate.change_layout(layout={v : G_original[partial_perm(p,v,n)].get_center() for v in G.vertices}), run_time=1)
        self.play(Write(string_eq[4:]))
        self.wait()
        self.clear()

    def apply_permutation_sequence(self, p_sequence, p_sequence_tex, s):
        G = Tree(3, len(s), width=13.5, vertex_config={s : {"fill_color": RED}} ).to_edge(UP)
        G_original = G.copy()
        string = s
        string_eq = MathTex( p_sequence_tex[0], "(", s, ")", "=", p_sequence[0](s) ).to_edge(DOWN)

        self.add(G)
        self.play(Write(string_eq[:4]))
        self.wait(0.8)
        for i in range(len(p_sequence)):
            if i == 0:
                pass
            else:
                self.play(*[Write(string_eq[j]) for j in [0,1,3]])
            p = p_sequence[i]
            for n in range(1,len(s)+1):
                self.play(G.animate.change_layout(layout={v : G_original[partial_perm(p,v,n)].get_center() for v in G.vertices}), run_time=1)
            self.play(Write(string_eq[-2:]))
            self.wait(0.5)
            if i != len(p_sequence)-1:
                new_string = p(string)
                new_string_eq = MathTex( p_sequence_tex[i+1], "(", new_string, ")", "=", p_sequence[i+1](new_string)).to_edge(DOWN)
                self.play(
                    FadeOut(string_eq[:-1]),
                    ReplacementTransform(string_eq[-1], new_string_eq[2])
                )
                string = new_string
                string_eq = new_string_eq
                self.remove(G)
                G = Tree(3, len(s), width=13.5, vertex_config={new_string : {"fill_color": RED}} ).to_edge(UP)
                G_original = G.copy()
                self.add(G)

        self.wait()


            



