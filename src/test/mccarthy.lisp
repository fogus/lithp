(label null (lambda (x)
              (eq x (quote ()))))

(label and (lambda (x y)
             (cond (x
                     (cond (y (quote t))
                           (t (quote ()))))
                   (t (quote ())))))

(label not (lambda (x)
             (cond (x (quote ()))
                   (t (quote t)))))

(label append (lambda (x y)
                (cond ((null x) y)
                      (t (cons (car x) (append (cdr x) y))))))
