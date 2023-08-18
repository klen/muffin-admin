import { useDataProvider } from "react-admin"
import { useMutation } from "react-query"

export function useAction(resource, action) {
  const dataProvider = useDataProvider()
  return useMutation<{ data: any }, { message: string } | string, any>((params: any) =>
    dataProvider.runAction(resource, action, params)
  )
}
