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

(label list (lambda (x y)
              (cons x (cons y (quote ())))))

(label pair (lambda (x y)
              (cond ((and (null x) (null y)) (quote ()))
                    ((and (not (atom x)) (not (atom y)))
                     (cons (list (car x) (car y))
                           (pair (cdr x) (cdr y)))))))

(label assoc (lambda (x y)
               (cond ((eq (car (car y)) x) (car (cdr (car y))))
                     (t (assoc x (cdr y))))))
