When running a lambda against the same variable more than once at the top level issues arise:

    (label x (pair (quote (a)) (quote (1))))
    (label x (pair (quote (a)) (quote (1))))

Will give ((a 1 a 1)) as the value of x.

-m


