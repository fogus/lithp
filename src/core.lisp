(label t (quote t))
(label nil (quote ()))

(label and (lambda (and_x and_y)
             (cond (and_x
                    (cond (and_y t)
                          (t nil)))
                   (t nil))))

(label not (lambda (not_x)
             (cond (not_x nil)
                   (t t))))

(label nand (lambda (nand_x nand_y)
              (not (and nand_x nand_y))))

(label or (lambda (or_x or_y)
            (nand
             (nand or_x or_x)
             (nand or_y or_y))))

(label nor (lambda (nor_x nor_y)
             (not (or nor_x nor_y))))

(label xor (lambda (xor_x xor_y)
             (or
              (and xor_x (not xor_y))
              (and (not xor_x) xor_y))))

(label and_ (lambda (x y) (cond (x (cond (y t) (t nil))) (t nil))))
(label not_ (lambda (x) (cond (x nil) (t t))))
(label nand_ (lambda (x y) (not_ (and_ x y))))
(label or_ (lambda (x y) (nand_ (nand_ x x) (nand_ y y))))
(label xor_ (lambda (x y) (or_ (and_ x (not_ y)) (and_ (not_ x) y))))

(label pair (lambda (x y)
              (cons x (cons y nil))))

(label zip (lambda (x y)
              (cond ((and (null x) (null y)) nil)
                    ((and (not (atom x)) (not (atom y)))
                     (cons (pair (car x) (car y))
                           (zip (cdr x) (cdr y)))))))

(label lookup (lambda (name context)
                (cond ((eq (car (car context)) name) (car (cdr (car context))))
                       (t (lookup name (cdr context))))))

(label caar (lambda (x) (car (car x))))
(label cadr (lambda (x) (car (cdr x))))
(label caddr (lambda (x) (car (cdr (cdr x)))))
(label cadar (lambda (x) (car (cdr (car x)))))
(label caddar (lambda (x) (car (cdr (cdr (car x))))))
(label cadddar (lambda (x) (car (cdr (cdr (cdr (car x)))))))

(label null (lambda (null_x)
              (eq null_x nil)))

(label mapcar (lambda (mapcar_f mapcar_lst)
                (cond
                  ((null mapcar_lst) mapcar_lst)
                  (t (cons
                      (mapcar_f (car mapcar_lst))
                      (mapcar mapcar_f (cdr mapcar_lst)))))))

(label reduce (lambda (reduce_f reduce_lst)
                (cond
                  ((null reduce_lst) (reduce_f))
                  (t (reduce_f (car reduce_lst)
                               (reduce reduce_f (cdr reduce_lst)))))))

(label append (lambda (append_x append_y)
                (cond ((null append_x) append_y)
                      (t (cons (car append_x) 
                               (append (cdr append_x) append_y))))))

(label filter (lambda (filter_f filter_lst)
                (cond
                  ((null filter_lst) filter_lst)
                  (t (cond
                       ((filter_f (car filter_lst)) (cons
                                                     (car filter_lst) 
                                                     (filter filter_f (cdr filter_lst))))
                       (t (filter filter_f (cdr filter_lst))))))))

(label env' (pair (pair (quote t) (quote t)) 
		  (pair (quote nil) nil)))

(label quote' (lambda (qexpr)
                (car (cdr qexpr))))

(label atom' (lambda (aexpr abinds)
	       (atom (eval (car (cdr aexpr)) abinds))))

(label eq' (lambda (eexpr ebinds)
	     (eq (eval (car (cdr eexpr)) ebinds)
		 (eval (car (cdr (cdr eexpr))) ebinds))))

(label car' (lambda (caexpr cabinds)
	      (car (eval (car (cdr caexpr)) cabinds))))

(label cdr' (lambda (cdexpr cdbinds)
	      (cdr (eval (car (cdr cdexpr)) cdbinds))))

(label cons' (lambda (coexpr cobinds)
	       (cons   (eval (car (cdr coexpr)) cobinds)
		       (eval (car (cdr (cdr coexpr))) cobinds))))

(label eval-cond (lambda (condition condbinds)
                   (cond ((eval (car (car condition)) condbinds)
                          (eval (car (cdr (car condition))) condbinds))
                         (t (eval-cond (cdr condition) condbinds)))))

(label cond' (lambda (cndexpr cndbinds)
	       (eval-cond (cdr cndexpr) cndbinds)))

(label eval (lambda (expr binds)
              (cond
                ((atom expr) (lookup expr binds))
                ((atom (car expr))
                 (cond
                   ((eq (car expr) (quote quote)) (quote' expr))
                   ((eq (car expr) (quote atom))  (atom'  expr binds))
                   ((eq (car expr) (quote eq))    (eq'    expr binds))
                   ((eq (car expr) (quote car))   (car'   expr binds))
                   ((eq (car expr) (quote cdr))   (cdr'   expr binds))
                   ((eq (car expr) (quote cons))  (cons'  expr binds))
                   ((eq (car expr) (quote cond))  (cond'  expr binds))
                   (t (eval (cons (lookup (car expr) binds)
                                  (cdr expr))
                            binds))))
                ((eq (caar expr) (quote label))
                 (eval (cons (caddar expr) (cdr expr))
                       (cons (pair (cadar expr) (car expr)) binds)))
                ((eq (caar expr) (quote lambda))
                 (eval (caddar expr)
                       (append (zip (cadar expr) (eval-args (cdr expr) binds))
                               binds)))
                ((eq (caar expr) (quote macro))
                 (cond
                   ((eq (cadar expr) (quote lambda))
                    (eval (eval (car (cdddar expr))
                                (cons (pair (car (caddar expr)) 
                                             (cadr expr)) 
                                      binds))
                          binds)))))))

(label eval-args (lambda (eval-args_m eval-args_a)
                   (cond ((null eval-args_m) nil)
                         (t (cons (eval  (car eval-args_m) eval-args_a)
                                  (eval-args (cdr eval-args_m) eval-args_a))))))

(label apply (lambda (apply_name apply_args)
               ((pair apply_name (pair (quote quote) apply_args)))))


(label zero (lambda (s z) z))
(label one (lambda (s z) (s z)))
(label plus (lambda (m n) (lambda (f x) (m f (n f x)))))
