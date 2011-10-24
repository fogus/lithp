Lithp is a(nother) McCarthy Lisp interpreter (with macros too) written in the Python Programming Language.

*note: currently only the Python port is fully operational*

RIP John McCarthy 1927.09.04 - 2011.10.23

What The?!?
===========

My last true exposure to Lisp was during my college years.  Since then I have hacked away at a bit of ELisp, but even that was done in the spirit of immediacy.  With the resurgence of Lisp, thanks to the advocacy of [Mr. Paul Graham](http://www.paulgraham.com), I feel it is once again time to (re)learn the language.  However, times have changed; I have written my recursive algorithms, I have explored the beauty of closures, and I have touched on functional programming with the grace and emotion of a lover.  However, I fear that if I simply take up the task of (re)learning Lisp then I will take these notions for granted and not appreciate them fully as they relate to Lisp itself.  Therefore, I feel that my best chance for truly absorbing Lisp is the invent Lisp.  While the leg-work has already been done by such luminaries as [Mr. McCarthy][jmc], [Mr. Steele][steele], and [Mr. Sussman][sussman], it is my intention to approach their works as if they are newly minted and implement them within the Lithp interpreter.

[steele]: http://research.sun.com/people/mybio.php?uid=25706
[jmc]: http://www-formal.stanford.edu/jmc
[sussman]: http://swiss.csail.mit.edu/~gjs

Features
========
The Lithp interpreter provides the absolute core functions of McCarthy's original as outlined in his classical paper.  That is, there are only seven functions and two special forms.

Seven Functions
---------------
1.  `atom`
2.  `car`
3.  `cdr`
4.  `cond`
5.  `cons`
6.  `eq`
7.  `quote`

Two Special Forms
------------------
1. `label`
2. `lambda`

