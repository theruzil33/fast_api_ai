import { Toolbar, DeleteButton as StyledDeleteButton } from './index.styles'

interface DeleteButtonProps {
  count: number
  onDelete: () => void
}

function DeleteButton({ count, onDelete }: DeleteButtonProps) {
  return (
    <Toolbar>
      <StyledDeleteButton onClick={onDelete} disabled={count === 0}>
        Delete{count > 0 ? ` (${count})` : ''}
      </StyledDeleteButton>
    </Toolbar>
  )
}

export default DeleteButton
