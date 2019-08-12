from typing import List

import click


class NotRequiredIfOpt(click.Option):
    """
    https://stackoverflow.com/questions/44247099/click-command-line-interfaces-make-options-required-if-other-optional-option-is
    """

    def __init__(self, *args, **kwargs):
        self.not_required_if_opts: List[str] = kwargs.pop('not_required_if')
        self.not_required_if_opts = (self.not_required_if_opts
                                     if isinstance(self.not_required_if_opts, list)
                                     else [self.not_required_if_opts])

        assert self.not_required_if_opts, '\'not_required_if\' parameter must be set'

        option_help_str = kwargs['help'] + '. ' if 'help' in kwargs else ''
        exclusive_opts_str = f"[{', '.join(self.not_required_if_opts)}]"
        kwargs['help'] = f"{option_help_str}Mutually exclusive with {exclusive_opts_str}".strip()

        super(NotRequiredIfOpt, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if_opts:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(f'Illegal usage: \'{self.name}\' is mutually exclusive with \'{mutex_opt}\'')
                else:
                    self.prompt = None
        return super(NotRequiredIfOpt, self).handle_parse_result(ctx, opts, args)
