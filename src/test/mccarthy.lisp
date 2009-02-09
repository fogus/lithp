(label null (lambda (x)
              (eq x (quote ()))))

(label and (lambda (x y)
             (cond (x
                     (cond (y (quote t))
                           (t (quote ()))))
                   (t (quote ())))))
