import { Transform } from 'class-transformer';
import { IsNumber } from 'class-validator';

export class BookFilterDto {
  @IsNumber({}, { message: 'validation.IS_NUMBER' })
  @Transform(({ value }) => +value)
  id: number;
}
