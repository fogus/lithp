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

(label caar (lambda (x) (car (car x))))
(label cadr (lambda (x) (car (cdr x))))
(label caddr (lambda (x) (car (cdr (cdr x)))))
(label cadar (lambda (x) (car (cdr (car x)))))
(label caddar (lambda (x) (car (cdr (cdr (car x))))))

(label eval (lambda (e a)
  (cond
    ((atom e) (assoc e a))
    ((atom (car e))
     (cond
       ((eq (car e) (quote quote)) (cadr e))
       ((eq (car e) (quote atom))  (atom   (eval (cadr e) a)))
       ((eq (car e) (quote eq))    (eq     (eval (cadr e) a)
                                    (eval (caddr e) a)))
       ((eq (car e) (quote car))   (car    (eval (cadr e) a)))
       ((eq (car e) (quote cdr))   (cdr    (eval (cadr e) a)))
       ((eq (car e) (quote cons))  (cons   (eval (cadr e) a)
                                    (eval (caddr e) a)))
       ((eq (car e) (quote cond))  (evcon (cdr e) a))
       (t (eval (cons (assoc (car e) a)
                        (cdr e))
                  a))))
    ((eq (caar e) (quote label))
     (eval (cons (caddar e) (cdr e))
            (cons (list (cadar e) (car e)) a)))
    ((eq (caar e) (quote lambda))
     (eval (caddar e)
            (append. (pair (cadar e) (evlis (cdr e) a))
                     a))))))

