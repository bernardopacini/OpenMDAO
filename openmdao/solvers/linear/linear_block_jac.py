"""Define the LinearBlockJac class."""
from openmdao.solvers.solver import BlockLinearSolver


class LinearBlockJac(BlockLinearSolver):
    """
    Linear block Jacobi solver.
    """

    SOLVER = 'LN: LNBJ'

    def _iter_execute(self):
        """
        Perform the operations in the iteration loop.
        """
        system = self._system
        mode = self._mode
        rhs_names = self._rhs_names

        if mode == 'fwd':
            for vec_name in rhs_names:
                system._transfer(vec_name, mode)
            for subsys in system._subsystems_myproc:
                scope_out, scope_in = system._get_scope(subsys)
                subsys._apply_linear(rhs_names, mode, scope_out, scope_in)
            for vec_name in rhs_names:
                b_vec = system._vectors['residual'][vec_name]
                b_vec *= -1.0
                b_vec += self._rhs_vecs[vec_name]
            for subsys in system._subsystems_myproc:
                subsys._solve_linear(rhs_names, mode)
        elif mode == 'rev':
            for subsys in system._subsystems_myproc:
                scope_out, scope_in = system._get_scope(subsys)
                subsys._apply_linear(rhs_names, mode, scope_out, scope_in)
            for vec_name in rhs_names:
                system._transfer(vec_name, mode)

                b_vec = system._vectors['output'][vec_name]
                b_vec *= -1.0
                b_vec += self._rhs_vecs[vec_name]
            for subsys in system._subsystems_myproc:
                subsys._solve_linear(rhs_names, mode)
