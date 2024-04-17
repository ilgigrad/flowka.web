
delete from filer_file_perms where file_id in (select id from filer_file where _type<>1);
delete from filer_folder_file where file_id in (select id from filer_file where _type<>1);
delete from filer_file_subjects where file_id in (select id from filer_file where _type<>1);
delete from datacollect_dataset_column where dataset_id in
	(select id from datacollect_dataset where datafile_id in
		(select id from filer_file where _type<>1));
delete from datacollect_dataset where datafile_id in (select id from filer_file where _type<>1);
delete from datacollect_column;
delete from filer_file where _type<>1;


delete from filer_file_perms where file_id in (select id from filer_file where _type=1);
delete from filer_folder_file where file_id in (select id from filer_file where _type=1);
delete from filer_file_subjects where file_id in (select id from filer_file where _type=1);
delete from filer_file where _type=1;
